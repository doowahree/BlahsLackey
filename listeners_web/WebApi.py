from flask import Flask

from databases.DatabaseRegistry import DatabaseRegistry
from listeners_web.wordle.WordleWebApi import WordleWebApi


class AllWebApi(object):
    def __init__(self, db_registry: DatabaseRegistry):
        self.all_api = [
            WordleWebApi(db_registry.wordle_db)
        ]

    def RegisterAppEndpoints(self, app: Flask):
        for api in self.all_api:
            api.RegisterEndpoints(app)
