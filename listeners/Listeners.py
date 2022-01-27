import re
from traceback import print_exc

from CommandParser import Command, CommandSet, TokenMatcherSet, TokenMatcher
from DiscordGateway import DiscordSession
from DiscordMessageTypes import MessageCreate
from GlobalDatabase import _GlobalDatabase
from listeners.ListenerMapping_pb2 import ListenerMapping
from databases.wordle.WordleDatabase import WordleDatabase
from listeners.wordle.WordleListener import WordleListener


class AllListeners(object):
    METADATA_NAME = 'listeners.metadata'

    def __init__(self, proto_store: _GlobalDatabase):
        self.proto_store = proto_store
        self.listener_mapping = ListenerMapping()
        self.load()
        self.listeners = {
            'Wordle': WordleListener(WordleDatabase(proto_store=proto_store))
        }
        self.commands = CommandSet([
            Command([self.help],
                    TokenMatcherSet([TokenMatcher('help')]),
                    help='This command'),
            Command([self.register_listener],
                    TokenMatcherSet([TokenMatcher('listen'),
                                     TokenMatcher(re.compile('[\\w]{,20}'), token_parsing=('listener_type', str))]),
                    help='Registers this channel to listen to the commands of: [%s]' % ','.join(self.listeners.keys())),
            Command([self.unregister_listener],
                    TokenMatcherSet([TokenMatcher('unlisten'),
                                     TokenMatcher(re.compile('[\\w]{,20}'), token_parsing=('listener_type', str))]),
                    help='Registers this channel to listen to the commands of: [%s]' % ','.join(self.listeners.keys())),
        ])

    def load(self):
        metadata = self.proto_store.LoadProto(AllListeners.METADATA_NAME)
        if metadata:
            self.listener_mapping = ListenerMapping()
            self.listener_mapping.ParseFromString(metadata)
        else:
            print('No original listener mapping, doing nothing.')

    def save(self):
        self.proto_store.StoreProto(AllListeners.METADATA_NAME, self.listener_mapping)

    def help(self, msg: MessageCreate, ds: DiscordSession):
        embeds = [{
            'title': '@AegisBot <commands>',
            'fields':
                [{'name': command, 'value': help_str} for help_str, command
                 in sorted(self.commands.help_strings())]
        }]
        ds.send_message(msg.channel_id,
                        '', embeds=embeds)

    def register_listener(self, msg: MessageCreate, ds: DiscordSession, listener_type: str = None):
        if listener_type in self.listeners:
            if listener_type in self.listener_mapping.channel_to_listener_mapping[msg.channel_id].listeners:
                ds.send_message(msg.channel_id, '[%s] command already activated for this channel' % listener_type)
            else:
                self.listener_mapping.channel_to_listener_mapping[msg.channel_id].listeners.append(listener_type)
                ds.send_message(msg.channel_id, '[%s] command listeners activated for this channel' % listener_type)
                self.save()
        else:
            ds.send_message(msg.channel_id, 'No such listeners...')

    def unregister_listener(self, msg: MessageCreate, ds: DiscordSession, listener_type: str = None):
        if listener_type in self.listeners:
            if listener_type in self.listener_mapping.channel_to_listener_mapping[msg.channel_id].listeners:
                self.listener_mapping.channel_to_listener_mapping[msg.channel_id].listeners.remove(listener_type)
                ds.send_message(msg.channel_id, '[%s] command disabled for this channel' % listener_type)
                self.save()
            else:
                ds.send_message(msg.channel_id,
                                '[%s] command listeners were never activated for this channel' % listener_type)
        else:
            ds.send_message(msg.channel_id, 'No such listeners...')

    def on_message(self, ds: DiscordSession, msg: MessageCreate):
        bot_id = ds.get_bot_info().id
        try:
            if bot_id in [m.id for m in msg.mentions]:
                self.commands.Apply(msg.content.split('>', 1)[1], additional_args={'msg': msg, 'ds': ds})
            for listener in self.listener_mapping.channel_to_listener_mapping[msg.channel_id].listeners:
                if listener in self.listeners:
                    self.listeners[listener].on_message(ds, msg)

        except Exception as e:
            print_exc()
