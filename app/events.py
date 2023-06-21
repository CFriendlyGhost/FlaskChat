import datetime as dt
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session
from flask_login import current_user
from database import data_loader

socketio = SocketIO()


@socketio.on("connect")
def handle_connection():
    username = current_user.username
    room = session.get("room_id")
    join_room(room)
    message = {"user": username, "message": "has joined the conversation"}

    emit(
        "message",
        message,
        broadcast=True,
        to=room,
    )


@socketio.on("disconnect")
def handle_disconnect():
    username = current_user.username
    room = session.get("room_id")
    leave_room(room)
    message = {"user": username, "message": "has left the conversation"}

    emit(
        "message",
        message,
        broadcast=30,
        to=room,
    )


@socketio.on("message")
def handle_message(data):
    room = session.get("room_id")
    username = current_user.username

    message = {"user": username, "message": data["data"]}

    emit(
        "message",
        message,
        broadcast=30,
        to=room,
    )
    data_loader.load_message(
        room_data=room,
        user_data=username,
        message_data=message["message"],
        message_time=dt.datetime.now(),
    )
