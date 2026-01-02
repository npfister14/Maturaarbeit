import json
import os
from app.models.user import User
from flask import redirect

USERS_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'users', 'users.json')

def get_username_by_token(token):
    #token zu username, eig deprecated aber nd überall entfernt, wip halt
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
    except Exception:
        return None
    for user in users:
        if user.get('token') == token:
            return user.get('username')
    return None


def is_logged_in(request):
    #luegt ob igloggt, wenn ja, return user
    token = request.cookies.get("user_token")
    if not token:
        return None

    username = get_username_by_token(token)
    if not username:
        # token existiert aber isch ungültig/abglaufe
        return None

    return User(username=username)