from . import db
from flask_login import UserMixin

user_in_rooms = db.Table(
    "user_in_rooms",
    db.Column("room_id", db.Integer, db.ForeignKey("rooms.room_id")),
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
)


class Room(db.Model):
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_code = db.Column(db.String(55))
    users = db.relationship("User", secondary=user_in_rooms, backref="rooms")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    confirmed = db.Column(db.Boolean, default=False, nullable=False)
    password = db.Column(db.String(255))
    messages = db.relationship("Message", backref="user")


class Message(db.Model):
    __tablename__ = "messages"
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255))
    send_time = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    room_code = db.Column(db.String, db.ForeignKey("rooms.room_code"))
