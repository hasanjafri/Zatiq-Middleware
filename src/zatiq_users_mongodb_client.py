from mongoengine import *
import secrets
import requests
import json
from models.zatiq_users import Zatiq_Users

class ZatiqUsersMongoDBClient(object):
    def get_all_users(self):
        all_users = []
        user1 = Zatiq_Users(user_email='scott@scottie.com', auth_token='scoot', user_name="Scott", zatiq_token='iamscott').save()
        for user in Zatiq_Users.objects:
            all_users.append(user)
        return(json.dumps(all_users))

    def generate_zatiq_api_token(self):
        api_token = secrets.token_urlsafe(32)
        if (self.check_api_token_exists(api_token) == False):
            return(api_token)
        else:
            self.generate_zatiq_api_token()

    def check_api_token_exists(self, api_token):
        pass
        