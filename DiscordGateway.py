import json
import os
import urllib.parse
import zlib
from queue import Queue
from sys import path
from time import sleep
import base64
from typing import List, Dict, Callable, Tuple

import websocket
import threading
import requests
from requests import Response

from DiscordMessageTypes import MessageCreate, User, DiscordEmoji

ZLIB_SUFFIX = b'\x00\x00\xff\xff'
ZLIB_INFLATOR = zlib.decompressobj()


class DiscordMessageQueuer(object):
    """Discord can only handle up to 50 api calls per second."""

    def __init__(self, rate_limit_qps: int = 10):
        """
        :param rate_limit_qps: Default of 40 to be well within limit.
        """
        self.delay_between_calls = 1.0 / rate_limit_qps
        self.queue: Queue.queue[Tuple[Callable, any, any]] = []
        self.lock = threading.RLock()
        self.timer = None

    def queue_call(self, fn: Callable, *args, **kwargs):
        self.queue.append((fn, args, kwargs))
        with self.lock:
            if not self.timer:
                self.timer = threading.Timer(self.delay_between_calls, self._handle)
                self.timer.start()

    def _handle(self):
        if len(self.queue):

            popped_item = self.queue.pop()
            print('Handling', popped_item)
            response: Response = popped_item[0](*popped_item[1], **popped_item[2])
            if response.status_code / 100 != 2:
                print(response)
                print(response.text)
            with self.lock:
                if len(self.queue):
                    self.timer = threading.Timer(self.delay_between_calls, self._handle)
                    self.timer.start()
                else:
                    self.timer = None


class DiscordSession(object):
    """Keeps sessions, responds to heartbeat requests, and sends heartbeats to keep conn alive."""

    def __init__(self, bot_token: str):
        self._ws: websocket.WebSocketApp = None
        self._bot_token: str = bot_token
        self._session_token: str = ''
        self._heartbeat_interval_ms: int = 45000
        self._last_seq_no: int = -1
        self._heartbeat_timer: threading.Timer = None
        self._queue_discord = DiscordMessageQueuer()

        # Http related
        self._header = {
            'Authorization': 'Bot %s' % self._bot_token,
            'User-Agent': 'DiscordBot(https://discord.gg/3DDf4kCR, 0.0)'
        }

        # Public
        self.bot_info = {}
        self.bot_user = None
        self.responders = {}

        self._should_reconnect = False;

    def send(self, json_msg):
        self._ws.send(json.dumps(json_msg))

    def save_session(self):
        with open('storage/cache.json', 'w') as f:
            to_write = {
                'session_token': self._session_token,
                'last_seq_no': self._last_seq_no,
                'bot_info': self.bot_info
            }
            json.dump(to_write, f)

    def heartbeat(self):
        """Sends a heartbeat and queues a new timer to send the next heartbeat."""
        print('sending heartbeat')
        self.send({"op": 1, "d": "null" if self._last_seq_no < 0 else self._last_seq_no})
        self._heartbeat_timer = threading.Timer(self._heartbeat_interval_ms / 1000, self.heartbeat)
        self._heartbeat_timer.start()

    def identify(self):
        """Sends identify request. Note you are limited to 1000 identify request per 24 hr rolling period."""
        self.send({
            'op': 2,
            'd': {
                'token': self._bot_token,
                'intents': 1 << 0 | 1 << 9 | 1 << 10,
                'properties': {
                    '$os': 'windows',
                    '$browser': 'disco',
                    'device': 'disco'
                },

            }
        })

    def get_bot_info(self) -> User:
        if not self.bot_user:
            self.bot_user = User(self.bot_info['user']['username'], self.bot_info['user']['id'], True)
        return self.bot_user

    def resume(self):
        """Tries to resume using stored session id."""
        if os.path.exists('storage/cache.json') and os.path.getsize('storage/cache.json') > 10:
            with open('storage/cache.json') as f:
                saved_data = json.load(f)
                self._session_token = saved_data['session_token']
                self._last_seq_no = saved_data['last_seq_no']
                self.bot_info = saved_data['bot_info']
            self.send({
                'op': 6,
                'd': {
                    'token': self._bot_token,
                    'session_id': self._session_token,
                    'seq': self._last_seq_no
                }
            })
            print('Resuming')
            return
        self.identify()
        print('Could not find stored session, starting new identify')

    def on_message(self, ws, message):
        payload = json.loads(message)
        if payload['op'] == 10:
            self._heartbeat_interval_ms = payload['d']['heartbeat_interval']
            if self._heartbeat_timer:
                self._heartbeat_timer.cancel()
            self.heartbeat()
            self.resume()
        elif payload['op'] == 9:
            # When invalid session, make sure to just reidentify instead.
            self.identify()
        elif payload['op'] == 7:
            self._ws.close()
            self._should_reconnect = True
        elif payload['op'] == 1:
            # When we have a op code 1, we need to immediately send a heartbeat back.
            if self._heartbeat_timer:
                self._heartbeat_timer.cancel()
            self.heartbeat()
        elif payload['op'] == 0:
            self._last_seq_no = payload['s']
            event_type = payload['t']
            if event_type == 'READY':
                self.bot_info = payload['d']
                self._session_token = payload['d']['session_id']
                self.save_session()
                # self.send_message('')
            if event_type == 'MESSAGE_CREATE':
                msg = MessageCreate(payload)
                if event_type in self.responders:
                    for item in self.responders[event_type]:
                        item(self, msg)
                pass

        print(payload)

    def send_message(self, channel_id: str, content: str, embeds: List[Dict[str, str]] = None):
        full_content = {'content': '%s' % content}
        if embeds:
            full_content['embeds'] = embeds
        self._queue_discord.queue_call(requests.post, 'https://discord.com/api/v9/channels/%s/messages' % channel_id,
                                       json=full_content,
                                       headers=self._header)

    def attach_reaction(self, message: MessageCreate, emoji: DiscordEmoji):
        self._queue_discord.queue_call(requests.put,
                                       'https://discord.com/api/v9/channels/%s/messages/%s/reactions/%s/@me' % (
                                           message.channel_id, message.id, urllib.parse.quote_plus(emoji.value)),
                                       headers=self._header)

    def run(self):
        """STarts up a websocket connecting to discord api"""
        while self.run:
            self._should_reconnect = False
            self._ws = websocket.WebSocketApp("wss://gateway.discord.gg/?v=9&encoding=json",
                                              on_open=on_open,
                                              on_message=self.on_message,
                                              on_error=on_error,
                                              on_close=self.on_close)

            self._ws.run_forever()
            sleep(5)

    def on_close(ws, close_status_code, close_msg):
        print('Close receieved, attempting to reconnect')
        print(close_msg)


def on_message(ws, message):
    payload = json.loads(message)
    if (payload['op'] == 10):
        print('Hearbeat')


def on_error(ws, error):
    print("ERROR")
    print(error)


def on_open(ws):
    print("Conn")


def RunWebsocketForever():
    pass
