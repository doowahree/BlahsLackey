from GlobalDatabase import _GlobalDatabase
from databases.wordle.WordleDatabase import WordleDatabase


class DatabaseRegistry(object):
    def __init__(self, global_db: _GlobalDatabase):
        self.proto_store: _GlobalDatabase = global_db
        self.wordle_db: WordleDatabase = WordleDatabase(global_db)
