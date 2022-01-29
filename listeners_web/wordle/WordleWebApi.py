from flask import Flask
import base64

from databases.wordle.WordlDb_pb2 import WordleSeason
from databases.wordle.WordleDatabase import WordleDatabase


class WordleWebApi(object):
    def __init__(self, wordle_db: WordleDatabase):
        self.wordle_db = wordle_db

    def RegisterEndpoints(self, app: Flask):
        @app.route('/api/wordle/get_season')
        def GetSeason():
            return {'data': str(self.wordle_db.wordle_season.SerializeToString(), 'utf-8')}

    def GetSeason(self) -> WordleSeason:
        return self.wordle_db.wordle_season