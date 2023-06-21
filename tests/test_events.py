import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from app import create_app


def run_socketio():
    app = create_app()
    socketio = app.extensions['socketio']
    client = socketio.test_client(app)
    socketio.emit('connect', namespace='/')
    socketio.emit('message', {'data': 'Test message'}, namespace='/')
    socketio.emit('disconnect', namespace='/')
    received_events = client.get_received('/')
    return client, received_events


def test_connection():
    client, received_events = run_socketio()
    connect_info = received_events[0]['name']
    client.disconnect()
    assert connect_info == 'connect'


def test_message():
    client, received_events = run_socketio()
    name = received_events[1]['name']
    data = received_events[1]['args']['data']
    client.disconnect()
    assert name == 'message'
    assert data == 'Test message'


def test_disconnection():
    client, received_events = run_socketio()
    disconnect_info = received_events[2]['name']
    client.disconnect()
    assert disconnect_info == 'disconnect'
