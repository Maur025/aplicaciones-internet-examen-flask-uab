import socketio
from flask import Flask

from .services.metric_service import add_metrics
from .services.server_service import add_servers

WS_CLIENT_HOST = 'http://localhost:9000'
sio = socketio.Client(reconnection=True, reconnection_attempts=15, reconnection_delay=10, reconnection_delay_max=20)

flask_app: Flask | None = None


@sio.event
def connect():
    print(f'[SOCKET-CLIENT] client connected to {WS_CLIENT_HOST}')


@sio.event
def disconnect():
    print('[SOCKET-CLIENT] client disconnected')


@sio.on('initialize')
def initialize(data):
    print(data)
    if flask_app:
        try:
            with flask_app.app_context():
                add_servers(data['servers'])

                print('EMITING TO SERVER')
                sio.emit('trigger:create:metrics', {'message': 'listo'})
        except Exception as ex:
            print(f'[SOCKET-CLIENT] Error processing data servers in Flask app context: {ex}')

    else:
        print('[SOCKET-CLIENT] Flask app context is not available. Cannot process data.')


@sio.on('metrics:create')
def metrics_create_socket(data):
    if flask_app:
        try:
            with flask_app.app_context():
                add_metrics(data)
        except Exception as ex:
            print(f'[SOCKET-CLIENT] Error processing data metrics in Flask app context: {ex}')

    else:
        print('[SOCKET-CLIENT] Flask app context is not available. Cannot process data.')


def connect_socket_client(app):
    global flask_app
    flask_app = app

    if not sio.connected:
        try:
            sio.connect(WS_CLIENT_HOST)
        except Exception as ex:
            print(f'[SOCKET-CLIENT] connect failed with exception: {ex}')
