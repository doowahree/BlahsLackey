# This is a sample Python script.
import os
from flask import Flask, send_from_directory
import threading
import websocket
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


app = Flask(__name__, static_folder='angular/webview/dist/webview/')
from DiscordGateway import RunWebsocketForever, DiscordSession
from GlobalDatabase import GlobalDatabase


# Press the green button in the gutter to run the script.
from listeners.Listeners import AllListeners
from listeners.wordle.WordlDb_pb2 import WordlSeasonFileDb
from listeners.wordle.WordleDatabase import WordleDatabase
from listeners.wordle.WordleListener import WordleListener



if __name__ == '__main__':

    ds = DiscordSession(os.environ['bot_token'])
    ds.responders['MESSAGE_CREATE'] = [AllListeners(proto_store=GlobalDatabase()).on_message]
    a = threading.Thread(target=app.run, kwargs={'port': 5000})
    a.start()
    ds.run()
    # print_hi('PyCharm')


