from sqlalchemy.exc import ProgrammingError
from database.database_creator import Room, Message, User
from . import db


def check_if_room_exist(room_code):
    room = db.session.query(Room).filter_by(room_code=room_code).first()
    return room is not None


def find_user_by_username(username):
    user = db.session.query(User).filter_by(username=username).first()
    return user


def find_user_by_email(email):
    user = db.session.query(User).filter_by(email=email).first()
    return user


def check_user_token_confirmation(username):
    user = find_user_by_username(username)
    if user is not None:
        return user.confirmed
    else:
        return False


def find_exact_message(room_code, username, message_time):
    message = (
        db.session.query(Message)
        .join(User)
        .join(Room)
        .filter(Room.room_code == room_code)
        .filter(User.username == username)
        .filter(Message.send_time == message_time)
        .first()
    )
    return message


def find_all_messages_in_room(room_code):
    try:
        room_messages = {}
        users_in_room = (
            db.session.query(User)
            .join(Room.users)
            .filter(Room.room_code == room_code)
            .all()
        )
        for user in users_in_room:
            users_messages = (
                db.session.query(Message.content, Message.send_time)
                .filter(Message.user_id == user.id)
                .filter(Message.room_code == room_code)
                .all()
            )
            room_messages[user.username] = users_messages
        return room_messages

    except ProgrammingError:
        return None
