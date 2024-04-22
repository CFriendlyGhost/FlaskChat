from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from flask_login import logout_user, login_user, login_required, current_user
from database import database_inquiries, data_loader
from werkzeug.security import generate_password_hash, check_password_hash
from email_service.token_service import generate_confirmation_token, confirm_token
from email_service.mail_sender import send_email

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    user = request.form.get("username")
    password = request.form.get("password")
    existing_user = database_inquiries.find_user_by_username(user)

    if not existing_user or not check_password_hash(existing_user.password, password):
        flash("Login details are incorrect.", "danger")
        return redirect(url_for("auth.login"))
    print(user)
    # if not database_inquiries.check_user_token_confirmation(user):
    #     flash("You need to confirm your account first.", "warning")
    #     return redirect(url_for("auth.login"))

    login_user(existing_user)
    return redirect(url_for("main.home"))


@auth_bp.route("/signup", methods=["GET"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    return render_template("signup.html")


@auth_bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    if password != confirm_password:
        flash("Passwords do not match.", "warning")
        return redirect(url_for("auth.signup"))

    password = generate_password_hash(password, method="sha256")

    if database_inquiries.find_user_by_username(username):
        flash("This username is already taken, if it's yours try to log in.", "warning")
        return redirect(url_for("auth.signup"))

    if database_inquiries.find_user_by_email(email):
        flash("This email is already taken.", "warning")
        return redirect(url_for("auth.signup"))

    data_loader.load_user(email=email, username=username, password=password)
    flash(
        "Successfully created account! Please check your mailbox and activate it.",
        "success",
    )

    token = generate_confirmation_token(username)
    confirmed_url = url_for("auth.confirm_email", token=token, _external=True)
    html = render_template("email.html", confirm_url=confirmed_url, username=username)
    send_email(email, html)
    return redirect(url_for("auth.login"))


@auth_bp.route("/confirm/<token>")
def confirm_email(token):
    try:
        username = confirm_token(token)
        user = database_inquiries.find_user_by_username(username)
        if user.confirmed:
            flash("Account already confirmed. Please login.", "success")
        else:
            data_loader.confirm_user_token(username)
            flash("You have confirmed your account. Thanks!", "success")
    except ConnectionError:
        flash("The confirmation link is invalid or has expired.", "warning")
    return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("auth.login"))
