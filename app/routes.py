from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_login import current_user
from . import scripts
from database import database_inquiries, data_loader
from .auth_routes import login_required

main_bp = Blueprint("main", __name__)


@main_bp.route("/home", methods=["GET", "POST"])
@login_required
def home():
    session.pop("room_id", None)
    return render_template("home.html")


@main_bp.route("/join_room", methods=["GET", "POST"])
@login_required
def join_room():
    if request.method == "POST":
        room_code = request.form.get("room_code")
        username = current_user.username

        if room_code == "":
            room_code = scripts.create_room_id(5)
            data_loader.load_room(room_data=room_code)
        elif database_inquiries.check_if_room_exist(room_code) is False:
            print(room_code)
            return render_template("join_room.html")

        session["room_id"] = room_code
        data_loader.load_user_to_room(
            room_data=room_code,
            user_data=username,
        )
        return redirect(url_for("main.chat"))

    return render_template(
        "join_room.html", recent_room_codes=scripts.rooms_to_codes(current_user.rooms)
    )


@main_bp.route("/create_room", methods=["GET"])
@login_required
def create_room():
    username = current_user.username
    room_code = scripts.create_room_id(5)
    data_loader.load_room(room_data=room_code)

    session["room_id"] = room_code
    data_loader.load_user_to_room(
        room_data=room_code,
        user_data=username,
    )
    return redirect(url_for("main.chat"))


@main_bp.route("/chat")
@login_required
def chat():
    room_id = session.get("room_id")
    if database_inquiries.check_if_room_exist(room_code=room_id):
        return render_template(
            "chat.html",
            code=room_id,
            messages=(
                scripts.change_dict_format(
                    database_inquiries.find_all_messages_in_room(room_code=room_id)
                )
            ),
        )
    else:
        return redirect(url_for("main.join_room"))
