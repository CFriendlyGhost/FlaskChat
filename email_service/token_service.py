from itsdangerous import URLSafeTimedSerializer
from app import SECRET_KEY, SECURITY_PASSWORD_SALT


def generate_confirmation_token(username):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(username, salt=SECURITY_PASSWORD_SALT)


def confirm_token(token):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    try:
        username = serializer.loads(
            token,
            salt=SECURITY_PASSWORD_SALT,
        )
    except ConnectionAbortedError:
        return False
    return username
