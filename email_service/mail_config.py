import json


def load_json():
    with open('passes.json', 'r') as file:
        data = json.load(file)
        return data


def configure_mail(app):
    passes = load_json()

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = passes["email"]
    app.config['MAIL_PASSWORD'] = passes["password"]
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
