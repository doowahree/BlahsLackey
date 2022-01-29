import re
from traceback import print_exc
from typing import Dict, Tuple

from CommandParser import Command, TokenMatcherSet, TokenMatcher, CommandSet
from DiscordGateway import DiscordSession
from DiscordMessageTypes import MessageCreate, DiscordEmoji
from databases.wordle.WordlDb_pb2 import UserRecord
from databases.wordle.WordleDatabase import WordleDatabase


class WordleListener(object):
    def __init__(self, wordle_db: WordleDatabase):
        self.wordle_db = wordle_db
        self.commands = CommandSet([
            Command([self.help],
                    TokenMatcherSet([TokenMatcher('help')]),
                    help='This command'),
            Command([self.print_weblink],
                    TokenMatcherSet([TokenMatcher('link')]),
                    help='Prints Wordle link and website link.'),
            Command([self.print_season],
                    TokenMatcherSet([TokenMatcher('season'), TokenMatcher('current', is_optional=True)]),
                    help='Prints the current season'),
            Command([self.change_season],
                    TokenMatcherSet([TokenMatcher('season'), TokenMatcher('change'),
                                     TokenMatcher(re.compile('[\\w\\d]{,40}'), token_parsing=('season', str))]),
                    help='Changes the season to <season>'),
            Command([self.register_custom],
                    TokenMatcherSet(
                        [TokenMatcher('register', is_optional=True),
                         TokenMatcher(re.compile('[\\w\\d]+'), token_parsing=('game_id', str)),
                         TokenMatcher(re.compile('[\\w\\d]+'), token_parsing=('attempts', self.int_or_neg_one)),
                         TokenMatcher('/'),
                         TokenMatcher(re.compile('\\d+'),
                                      token_parsing=('max_attempts', int)),
                         TokenMatcher(re.compile('.{,50}'),
                                      is_optional=True,
                                      token_parsing=('metadata', str))
                         ]
                    ),
                    help='Registers <game_id> with <attempts>/<max_attempts>. <metadata> is currently unused.'),
            Command([self.update_custom],
                    TokenMatcherSet(
                        [TokenMatcher('update'),
                         TokenMatcher(re.compile('[\\w\\d]+'), token_parsing=('game_id', str)),
                         TokenMatcher(re.compile('[\\w\\d]+'), token_parsing=('attempts', self.int_or_neg_one)),
                         TokenMatcher('/'),
                         TokenMatcher(re.compile('\\d+'),
                                      token_parsing=('max_attempts', int)),
                         TokenMatcher(re.compile('.{,50}'),
                                      is_optional=True,
                                      token_parsing=('metadata', str))
                         ]
                    ),
                    help='Updates <game_id> with <attempts>/<max_attempts>. <metadata> is currently unused.'),
            Command([self.delete_record],
                    TokenMatcherSet(
                        [TokenMatcher('delete'),
                         TokenMatcher(re.compile('[\\w\\d]+'), token_parsing=('game_id', str))
                         ]
                    ),
                    help='Deletes <game_id> from the record.'),
            Command([self.print_stats],
                    TokenMatcherSet(
                        [TokenMatcher('stats')]
                    ),
                    help='Prints the stats for yourself - limited to last x games.'),
            Command([self.leaderboard],
                    TokenMatcherSet(
                        [TokenMatcher('leaderboard')]
                    ),
                    help='Prints the leaderboard.')
        ])

    def print_weblink(self, msg: MessageCreate, ds: DiscordSession):
        ds.send_message(msg.channel_id,
                        'Play the game at: https://www.powerlanguage.co.uk/wordle/ \n'
                        'See full stats at: https://blahs-discord-bots.herokuapp.com/')

    def help(self, msg: MessageCreate, ds: DiscordSession):
        embeds = [{
            'title': 'Wordle <commands>',
            'fields':
                [{'name': command, 'value': help_str} for help_str, command
                 in sorted(self.commands.help_strings())]
        }]
        ds.send_message(msg.channel_id,
                        '', embeds=embeds)

    @staticmethod
    def int_or_neg_one(item: str):
        try:
            return int(item)
        except Exception as e:
            return -1

    def print_season(self, msg: MessageCreate, ds: DiscordSession):
        ds.send_message(msg.channel_id, 'Current season is [%s]' % self.wordle_db.wordle_season.name)

    def change_season(self, msg: MessageCreate, ds: DiscordSession, season: str):
        is_new_season, season_name, filename = self.wordle_db.change_season(season)
        if is_new_season:
            ds.send_message(msg.channel_id, 'New season has started! Current season: [%s]' % season)
        else:
            ds.send_message(msg.channel_id, 'Switching back to season: [%s] - filename: [%s]' % (season_name, filename))

    def register_custom(self, msg: MessageCreate, ds: DiscordSession, game_id: str, attempts: int, max_attempts: int,
                        metadata: str = ''):
        metadata = metadata or ''
        is_new, record = self.wordle_db.register_record(msg.author, game_id, attempts, max_attempts,
                                                        None if not metadata.startswith('@!@') else metadata)
        if is_new:
            ds.attach_reaction(msg, DiscordEmoji.symbol_ok)
            ds.attach_reaction(msg, DiscordEmoji.GetNumber(
                record.attempts) if record.attempts > 0 else DiscordEmoji.x)
        else:
            ds.attach_reaction(msg, DiscordEmoji.symbol_nope)

    def update_custom(self, msg: MessageCreate, ds: DiscordSession, game_id: str, attempts: int, max_attempts: int,
                      metadata: str = ''):
        success, record = self.wordle_db.update_record(msg.author, game_id, attempts, max_attempts,
                                                       None if not metadata.startswith('@!@') else metadata)
        if success:
            ds.attach_reaction(msg, DiscordEmoji.symbol_ok)
            ds.attach_reaction(msg, DiscordEmoji.GetNumber(
                record.attempts) if record.attempts > 0 else DiscordEmoji.x)
        else:
            ds.attach_reaction(msg, DiscordEmoji.symbol_nope)

    def delete_record(self, msg: MessageCreate, ds: DiscordSession, game_id: str):
        success, record = self.wordle_db.delete_record(msg.author, game_id)
        if success:
            ds.attach_reaction(msg, DiscordEmoji.symbol_ok)
        else:
            ds.attach_reaction(msg, DiscordEmoji.symbol_nope)

    def print_stats(self, msg: MessageCreate, ds: DiscordSession, season: str = None):
        ur: UserRecord = self.wordle_db.wordle_season.users[msg.author.id]
        topic = 'Status for [%s] - Last 9 games' % msg.author.username
        classic_games = []
        classic_games_attempts = {}
        custom_games = []
        classic_attempt_total = 0
        custom_attempt_total = 0
        embeds = []
        for game, rec in sorted(ur.classic_games.items(), key=lambda k: k[1].game, reverse=True):
            if rec.attempts not in classic_games_attempts:
                classic_games_attempts[rec.attempts] = 0
            classic_games_attempts[rec.attempts] += 1
            classic_attempt_total += rec.attempts if rec.attempts >= 0 else (rec.max_attempts + 1)
            if len(classic_games) < 9:
                classic_games.append(rec)
        for game, rec in sorted(ur.custom_games.items(), key=lambda k: k[1].game, reverse=True):
            custom_attempt_total += rec.attempts if rec.attempts >= 0 else (rec.max_attempts + 1)
            if len(classic_games) < 9:
                custom_games.append(rec)
        if classic_games:
            embeds.append(
                {
                    'title': 'Classic Games',
                    'description': 'Average attempt: %s over %s games' % (
                        classic_attempt_total / len(ur.classic_games), len(ur.classic_games)),
                    'fields':
                        [{'name': 'Count of Attempt: %s' % attempt, 'value': '%s' % count} for attempt, count
                         in sorted(classic_games_attempts.items())] +
                        [{'inline': True, 'name': r.game, 'value': '%s/%s' % (r.attempts, r.max_attempts)} for r
                         in classic_games]
                })
        if custom_games:
            embeds.append(
                {
                    'title': 'Custom Games',
                    'description': 'Average attempt: %s over %s games' % (
                        custom_attempt_total / len(ur.custom_games), len(ur.custom_games)),
                    'fields': [{'name': r.game, 'value': '%s/%s' % (r.attempts, r.max_attempts)} for r in custom_games]
                })
        ds.send_message(msg.channel_id, topic, embeds=embeds)

    def leaderboard(self, msg: MessageCreate, ds: DiscordSession, season: str = None):
        all_scores: Dict[str, Tuple[int, int, float]] = {}
        topic = 'Leaderboard (games played * number of games played - total attempts)'
        for user_id, ur in self.wordle_db.wordle_season.users.items():
            score = 0
            games_played = 0
            attempts = 0
            for game, rec in sorted(ur.classic_games.items(), key=lambda k: k[1].game, reverse=True):
                if game.startswith('_'):
                    continue
                attempts += (rec.attempts if rec.attempts >= 0 else (rec.max_attempts + 1))
                games_played += 1
                score += rec.max_attempts - (rec.attempts if rec.attempts >= 0 else (rec.max_attempts + 1))

            all_scores['%s(%s)' % (ur.last_known_name, user_id)] = (score, games_played, attempts / (games_played or 1))

        sorted_scores = sorted(all_scores.items(), key=lambda x: x[1][0], reverse=True)

        embeds = []
        if sorted_scores:
            embeds.append(
                {
                    'title': 'Classic Games',
                    'description': 'Top 15',
                    'fields': [{'name': '%d. %s' % (ranking, user_id),
                                'value': 'Score: %s -  Games Played: %s - Avg: %s' % (
                                    score_tuple[0], score_tuple[1], score_tuple[2])} for ranking, (user_id, score_tuple)
                               in
                               enumerate(sorted_scores, start=1)]
                })
        ds.send_message(msg.channel_id, topic, embeds=embeds)

    def on_message(self, ds: DiscordSession, msg: MessageCreate):
        try:
            if msg.content.startswith('Wordle') or msg.content.startswith('wordle'):
                self.commands.Apply(msg.content[6:], additional_args={'msg': msg, 'ds': ds})
        except Exception as e:
            print_exc()
