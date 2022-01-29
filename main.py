# This is a sample Python script.
import os
import threading

from flask import Flask, current_app

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from DiscordGateway import DiscordSession
from GlobalDatabase import GlobalDatabase

# Press the green button in the gutter to run the script.
from databases.DatabaseRegistry import DatabaseRegistry
from listeners.Listeners import AllListeners
from listeners_web.WebApi import AllWebApi

if __name__ == '__main__':
    database = GlobalDatabase()
    database_registry: DatabaseRegistry = DatabaseRegistry(database)
    ds = DiscordSession(os.environ['bot_token'], database)
    ds.responders['MESSAGE_CREATE'] = [AllListeners(database_registry).on_message]

    app = Flask(__name__, static_folder='angular/webview/dist/webview/')


    @app.route('/identify_client_id')
    def return_client_id():
        return {'client_id': os.environ['bot_client_id']}


    @app.route('/identify/<path:protocol>/<path:redirect_uri>/<path:path>')
    def identify(protocol: str, redirect_uri: str, path: str):
        return ds.proxy_oauth(protocol, redirect_uri, path)


    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def index(path: str = None):
        return current_app.send_static_file('index.html')


    AllWebApi(database_registry).RegisterAppEndpoints(app)
    a = threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': os.environ['PORT']})
    a.start()
    ds.run()
    # print_hi('PyCharm')
