import random
import secrets
import json
import os
import hashlib
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users', 'users.json')

class User:
    def __init__(self, username, email=None, password=None):
        #falls @ vorher trenne 
        if '@' in username:
            username = username.split('@')[0]
        self.username = username
        print("Initializing user:", username)
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
            user = next((u for u in users if u['username'] == username), None)
            if user:
                print("User found:", user)

                self.email = user.get('email')
                self.password = user.get('pwd')
                self.token = user.get('token')
                if self.token is None:
                    self.token = secrets.token_urlsafe(16)
                if email != None:
                    self.email = email
                if password != None:
                    self.password = password
            else:
                print("User not found, creating new user.")
                self.email = email
                self.password = password
                self.token = secrets.token_urlsafe(16)

    def generate_token(self):
        self.token = secrets.token_urlsafe(16)
        return self.token
    
    def save_user(self):
        with open(USERS_FILE, 'r+') as f:
            users = json.load(f)
            user = next((u for u in users if u['username'] == self.username), None)
            #hash
            print(self.password)
            self.password = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
            #falls es de user scho gitt, update
            if user:
                print("Updating user:", self.username)
                user['email'] = self.email
                user['pwd'] = self.password
                user['token'] = self.token
                #falls nöd, erstelle
            else:
                print("Creating new user:", self.username)
                users.append({
                    'username': self.username,
                    'email': self.email,
                    'pwd': self.password,
                    'token': self.token
                })
            f.seek(0)
            json.dump(users, f)
            f.truncate()

