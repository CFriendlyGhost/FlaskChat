from sqlalchemy.exc import IntegrityError
from database.database_inquiries import find_user_by_username
from database.database_creator import Room, User, Message
from . import db


def load_room(room_data):
    room = Room(room_code=room_data)
    try:
        db.session.add(room)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def confirm_user_token(user_data):
    user = find_user_by_username(user_data)
    if user is not None:
        user.confirmed = True
        db.session.commit()


def load_user_to_room(room_data, user_data):
    try:
        room = Room.query.filter_by(room_code=room_data).first()
        user = User.query.filter_by(username=user_data).first()
        if room is not None and user is not None:
            room.users.append(user)
            db.session.commit()
    except IntegrityError:
        db.session.rollback()


def load_user(email, username, password):
    try:
        user = User(
            email=email,
            username=username,
            password=password,
        )
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def load_message(room_data, user_data, message_data, message_time):
    try:
        room = Room.query.filter_by(room_code=room_data).first()
        user = User.query.filter_by(username=user_data).first()

        if room is not None and user is not None:
            message = Message(
                content=message_data,
                send_time=message_time,
                user_id=user.id,
                room_code=room_data,
            )
            db.session.add(message)
            db.session.commit()

    except IntegrityError:
        db.session.rollback()
