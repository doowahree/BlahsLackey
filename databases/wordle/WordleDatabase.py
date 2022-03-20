import random
import string
from typing import Tuple, Optional, List

from DiscordMessageTypes import User
from GlobalDatabase import GlobalDatabase, _GlobalDatabase
from databases.wordle.WordlDb_pb2 import WordleSeason, WordlSeasonFileDb, GameRecord, UserRecord, DailySeasonModifier

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)


class WordleDatabase(object):
    def __init__(self, proto_store: _GlobalDatabase):
        self.proto_store = proto_store or GlobalDatabase()
        self.wordle_metadata: WordlSeasonFileDb = WordlSeasonFileDb()
        self.wordle_season: WordleSeason = WordleSeason()
        self.load_filenames()

    def _metadata_name(self):
        return 'wordle.metadata'

    def _season_name(self, name):
        return 'wordle.seasons.%s' % name

    def load_filenames(self):
        metadata = self.proto_store.LoadProto(self._metadata_name())
        if metadata:
            self.wordle_metadata = WordlSeasonFileDb()
            self.wordle_metadata.ParseFromString(metadata)
            filename = self.wordle_metadata.current_file
            season_data = self.proto_store.LoadProto(self._season_name(filename))
            if season_data:
                self.wordle_season = WordleSeason()
                self.wordle_season.ParseFromString(season_data)
        else:
            print('No Wordle db, creating basic default')
            self.wordle_metadata.current_season_name = 'Tutorial'
            self.wordle_metadata.current_file = 'tutorial'
            self.wordle_season.name = 'Tutorial'
            self.wordle_season.filename = 'tutorial'
            self.wordle_metadata.filename_to_season_name['tutorial'] = 'Tutorial'

    def save_season(self):
        self.proto_store.StoreProto(self._season_name(self.wordle_metadata.current_file), self.wordle_season)

    def save_metadata(self):
        self.proto_store.StoreProto(self._metadata_name(), self.wordle_metadata)

    def hide_followup_register_channel(self, channel: str, do_hide: bool = True):
        self.wordle_metadata.reprint_registered[channel] = do_hide
        self.save_metadata()

    def hide_followup_check(self, channel: str) -> bool:
        return self.wordle_metadata.reprint_registered[
            channel] if channel in self.wordle_metadata.reprint_registered else False

    def mods_get_words(self, user: User) -> List[str]:
        return list(self.wordle_season.users[user.id].user_modifier.suggested_starters)

    def mods_set_words(self, user: User, words: str, word_constraint=5):
        words = words.strip()
        if words:
            split_words = words.split(',')
            valid_words = [w for w in split_words if len(w) == word_constraint][:5]
            invalid_words = [w for w in split_words if w not in valid_words]

            prev_words = self.mods_get_words(user)
            self.wordle_season.users[user.id].user_modifier.suggested_starters[:] = valid_words
            self.save_season()
            return [prev_words, valid_words, invalid_words]

    def mods_reroll(self, modifier_key: str) -> DailySeasonModifier:
        existing_modifier = [dm for dm in self.wordle_season.daily_modifier[:3] if dm.identifier == modifier_key]
        if any(existing_modifier):
            self.wordle_season.daily_modifier.remove(existing_modifier[0])
            return existing_modifier[0]
        else:
            return None

    def mods_get(self, modifier_key: str) -> DailySeasonModifier:
        existing_modifier = [dm for dm in self.wordle_season.daily_modifier[:3] if dm.identifier == modifier_key]
        if any(existing_modifier):
            return existing_modifier[0]
        else:
            dm = DailySeasonModifier()
            dm.identifier = modifier_key
            word_bag = {}
            for user, userRec in self.wordle_season.users.items():
                for w in userRec.user_modifier.suggested_starters:
                    if w not in word_bag:
                        word_bag[w] = []
                    word_bag[w].append('<@%s>' % user)
            if len(word_bag.items()) < 3:
                sampled_items = ['%s(%s)' % (word, ','.join(users)) for word, users in word_bag.items()]
            else:
                sampled_items = ['%s(%s)' % (word, ','.join(users)) for word, users in
                                 random.sample(word_bag.items(), 3)]
            dm.word_pool.extend(sampled_items)
            self.wordle_season.daily_modifier.insert(0, dm)
            self.save_season()
            return dm

    def change_season(self, season: str) -> Tuple[bool, str, str]:
        """
        Changes season.

        :param season: season to change to. Automatically sanitized.
        :return: is new season, season name, sanitized filename.
        """
        self.save_season()
        sanitized_filename = ''.join([c for c in season.lower()[:50] if c in valid_chars])
        if sanitized_filename in self.wordle_metadata.filename_to_season_name:
            self.wordle_metadata.current_season_name = season
            self.wordle_metadata.current_file = sanitized_filename
            self.save_metadata()
            self.load_filenames()

            return False, season, sanitized_filename
        else:
            self.wordle_season = WordleSeason(
                name=season,
                filename=sanitized_filename,
            )
            self.wordle_metadata.current_season_name = season
            self.wordle_metadata.current_file = sanitized_filename
            self.wordle_metadata.filename_to_season_name[sanitized_filename] = season
            self.save_season()
            self.save_metadata()
            self.load_filenames()
            return True, season, sanitized_filename

    def get_or_create_user(self, user: User) -> UserRecord:
        """Gets or creates a new user."""
        user_proto = self.wordle_season.users[user.id]
        user_proto.last_known_name = user.username
        return user_proto

    def register_record(self, author: User, game_id: str, attempt: int, max_tries: int, metadata=None) -> Tuple[
        bool, GameRecord]:
        """
        Tries to register a new record.

        :param author: The user calling this api.
        :param game_id: The game id.
        :param attempt: The attempts it took. -1 for didn't solve.
        :param max_tries: The max attempts given.
        :param metadata: Extra metadata for custom games.
        :return: successful register, the game record.
        """
        user = self.get_or_create_user(author)
        if game_id in user.classic_games:
            return False, user.classic_games[game_id]
        elif game_id in user.custom_games:
            return False, user.classic_games[game_id]
        else:
            rec = GameRecord(
                game=game_id,
                attempts=attempt,
                max_attempts=max_tries,
                extra_data=metadata
            )
            if metadata:
                user.custom_games[game_id].MergeFrom(rec)
            else:
                user.classic_games[game_id].MergeFrom(rec)
            self.save_season()
            return True, rec

    def update_record(self, author: User, game_id: str, attempt: int, max_tries: int, metadata=None) -> Tuple[
        bool, GameRecord]:
        """
        Tries to update a record.

        :param author: The user calling this api.
        :param game_id: The game id.
        :param attempt: The attempts it took. -1 for didn't solve.
        :param max_tries: The max attempts given.
        :param metadata: Extra metadata for custom games.
        :return: successful update, the game record.
        """
        rec = GameRecord(
            game=game_id,
            attempts=attempt,
            max_attempts=max_tries,
            extra_data=metadata
        )
        user = self.get_or_create_user(author)
        if game_id in user.classic_games:
            user.classic_games[game_id].MergeFrom(rec)
            self.save_season()
            return True, rec
        elif game_id in user.custom_games:
            user.custom_games[game_id].MergeFrom(rec)
            self.save_season()
            return True, rec
        else:
            return False, rec

    def delete_record(self, author: User, game_id: str) -> Tuple[bool, Optional[GameRecord]]:
        user = self.get_or_create_user(author)
        if game_id in user.classic_games:
            self.save_season()
            return True, user.classic_games.pop(game_id)
        elif game_id in user.custom_games:
            self.save_season()
            return True, user.custom_games.pop(game_id)
        else:
            return False, None
