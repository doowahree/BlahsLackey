import json
import os
import urllib.parse
import zlib
from queue import Queue
from sys import path
from time import sleep
import base64
import hashlib
from typing import List, Dict, Callable, Tuple

import websocket
import threading
import requests
from requests import Response

from DiscordMessageTypes import MessageCreate, User, DiscordEmoji
from GlobalDatabase import _GlobalDatabase

ZLIB_SUFFIX = b'\x00\x00\xff\xff'
ZLIB_INFLATOR = zlib.decompressobj()


class DiscordMessageQueuer(object):
    """Discord can only handle up to 50 api calls per second."""

    def __init__(self, rate_limit_qps: int = 3):
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
            with self.lock:
                if int(response.status_code / 100) != 2:

                    print(response.status_code, ' ', response.text)
                    if 'retry_after' in response.text:
                        print('Readding retry')
                        self.queue.insert(0, popped_item)
                if len(self.queue):
                    self.timer = threading.Timer(self.delay_between_calls, self._handle)
                    self.timer.start()
                else:
                    self.timer = None


class DiscordSession(object):
    """Keeps sessions, responds to heartbeat requests, and sends heartbeats to keep conn alive."""

    def __init__(self, bot_token: str, global_db: _GlobalDatabase):
        self.global_db = global_db
        self._ws: websocket.WebSocketApp = None
        self._bot_token: str = bot_token

        # Not a good idea to store tokens in database, hash it for half assed attempt at security.
        # But even if it's leaked, NBD.
        self._lookup_token: str = 'LookupToken.' + hashlib.sha256(self._bot_token.encode('utf-8')).hexdigest()
        self._session_token: str = ''
        self._heartbeat_interval_ms: int = 45000
        self._last_seq_no: int = -1
        self._heartbeat_timer: threading.Timer = None
        self._queue_discord = DiscordMessageQueuer()
        self._save_time: threading.Timer = None

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

    def _save_session(self):
        print('Saving session')
        to_write = {
            'session_token': self._session_token,
            'last_seq_no': self._last_seq_no,
            'bot_info': self.bot_info
        }

        self.global_db.StoreKeyVal(self._lookup_token, json.dumps(to_write))

    def save_session(self):
        """Schedules a save event.

        We schedule a save event to happen 5 seconds later. If a new save request comes, that
        """
        if self._save_time:
            self._save_time.cancel()
        self._save_time = threading.Timer(5, self._save_session)
        self._save_time.start()

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
        resume_token = self.global_db.LoadKeyVal(self._lookup_token)
        if resume_token:
            saved_data = json.loads(resume_token[1])
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
            if event_type == 'MESSAGE_CREATE':
                msg = MessageCreate(payload)
                if event_type in self.responders:
                    for item in self.responders[event_type]:
                        item(self, msg)
            self.save_session()

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

    def proxy_oauth(self, protocol: str, redirect_uri: str, code: str):
        print(redirect_uri)
        # http://192.168.1.3:5123/
        print(f'{protocol}//{redirect_uri}')
        print(code)
        r = requests.post('https://discord.com/api/v9/oauth2/token', data={
            'client_id': os.environ['bot_client_id'],
            'client_secret': os.environ['bot_client_secret'],
            'grant_type': 'authorization_code',
            'code': code,
            # http://192.168.1.3:5123/
            # f'{protocol}//{redirect_uri}'
            'redirect_uri': f'{protocol}//{redirect_uri}'},
                      headers={
                          'Content-Type': 'application/x-www-form-urlencoded'
                      }
                      )
        access_token_obj = json.loads(r.text)
        identify = requests.get('https://discord.com/api/v9/users/@me',
                     headers={
                         'Authorization': 'Bearer %s' % access_token_obj['access_token']
                     })

        access_token_obj['user'] = json.loads(identify.text)
        return access_token_obj


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
