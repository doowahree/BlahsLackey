import string
from typing import Tuple, Optional

from DiscordMessageTypes import User
from GlobalDatabase import GlobalDatabase, _GlobalDatabase
from databases.wordle.WordlDb_pb2 import WordleSeason, WordlSeasonFileDb, GameRecord, UserRecord

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)


class WordleDatabase(object):
    def __init__(self, proto_store: _GlobalDatabase):
        self.proto_store = proto_store or GlobalDatabase()
        self.wordle_season_pointer: WordlSeasonFileDb = WordlSeasonFileDb()
        self.wordle_season: WordleSeason = WordleSeason()
        self.load_filenames()

    def _metadata_name(self):
        return 'wordle.metadata'

    def _season_name(self, name):
        return 'wordle.seasons.%s' % name

    def load_filenames(self):
        metadata = self.proto_store.LoadProto(self._metadata_name())
        if metadata:
            self.wordle_season_pointer = WordlSeasonFileDb()
            self.wordle_season_pointer.ParseFromString(metadata)
            filename = self.wordle_season_pointer.current_file
            season_data = self.proto_store.LoadProto(self._season_name(filename))
            if season_data:
                self.wordle_season = WordleSeason()
                self.wordle_season.ParseFromString(season_data)
        else:
            print('No Wordle db, creating basic default')
            self.wordle_season_pointer.current_season_name = 'Tutorial'
            self.wordle_season_pointer.current_file = 'tutorial'
            self.wordle_season.name = 'Tutorial'
            self.wordle_season.filename = 'tutorial'
            self.wordle_season_pointer.filename_to_season_name['tutorial'] = 'Tutorial'

    def save_season(self):
        self.proto_store.StoreProto(self._season_name(self.wordle_season_pointer.current_file), self.wordle_season)

    def save_filenames(self):
        self.proto_store.StoreProto(self._metadata_name(), self.wordle_season_pointer)

    def change_season(self, season: str) -> Tuple[bool, str, str]:
        """
        Changes season.

        :param season: season to change to. Automatically sanitized.
        :return: is new season, season name, sanitized filename.
        """
        self.save_season()
        sanitized_filename = ''.join([c for c in season.lower()[:50] if c in valid_chars])
        if sanitized_filename in self.wordle_season_pointer.filename_to_season_name:
            self.wordle_season_pointer.current_season_name = season
            self.wordle_season_pointer.current_file = sanitized_filename
            self.save_filenames()
            self.load_filenames()

            return False, season, sanitized_filename
        else:
            self.wordle_season = WordleSeason(
                name=season,
                filename=sanitized_filename,
            )
            self.wordle_season_pointer.current_season_name = season
            self.wordle_season_pointer.current_file = sanitized_filename
            self.wordle_season_pointer.filename_to_season_name[sanitized_filename] = season
            self.save_season()
            self.save_filenames()
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
