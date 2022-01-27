# This is a sample Python script.
import os
import threading

from flask import Flask

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


app = Flask(__name__, static_folder='angular/webview/dist/webview/')
from DiscordGateway import DiscordSession
from GlobalDatabase import GlobalDatabase

# Press the green button in the gutter to run the script.
from listeners.Listeners import AllListeners

if __name__ == '__main__':
    database = GlobalDatabase()
    ds = DiscordSession(os.environ['bot_token'], database)
    ds.responders['MESSAGE_CREATE'] = [AllListeners(proto_store=database).on_message]
    a = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': os.environ['PORT']})
    a.start()
    ds.run()
    # print_hi('PyCharm')
