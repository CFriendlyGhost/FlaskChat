import datetime as dt
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import session
from flask_login import current_user
from database import data_loader
import base64
import io
import os
from PIL import Image
import uuid
from azure.storage.blob import BlobServiceClient, ContentSettings
import json
import mimetypes

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


def send_to_blob(file_name):
    with open('passes.json', 'r') as file:
        data = json.load(file)

    connection_string = data["connection_key"]
    photo_path = f"./app/static/{file_name}"

    container_name = "photos"
    content_type, _ = mimetypes.guess_type(photo_path)
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(file_name)

    with open(photo_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True, content_settings=ContentSettings(content_type=content_type))

    os.remove(photo_path)

    return blob_client.url

@socketio.on("image")
def handle_message(data):
    room = session.get("room_id")
    username = current_user.username

    base64_data = data["image"].split(",")[1]
    image_data = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(image_data))
    image = image.convert("RGB")
    file_name = str(uuid.uuid4())

    image.save(f"./app/static/{file_name}.png", format="PNG")
    photo_url = send_to_blob(f"{file_name}.png")
    message = {"user": username, "message": photo_url}

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

@socketio.on("typing")
def handle_typing():
    room = session.get("room_id")
    username = current_user.username

    typing_username = username
    emit(
        "typing",
        typing_username,
        broadcast=30,
        to=room,
    )


@socketio.on("stop_typing")
def handle_typing():
    room = session.get("room_id")
    username = current_user.username

    typing_username = username
    emit(
        "stop_typing",
        typing_username,
        broadcast=30,
        to=room,
    )
