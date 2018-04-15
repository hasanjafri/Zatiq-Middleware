from mongoengine import *
import secrets
import requests
import json
from zatiq_users import Zatiq_Users

class ZatiqUsersMongoDBClient(object):
    def get_all_users(self):
        all_users = []
        for user in Zatiq_Users.objects:
            all_users.append(user.user_name)
        print(all_users)
        return(json.dumps(all_users))
    
    def get_specific_user(self, api_token):
        user = Zatiq_Users.objects(zatiq_token=api_token)
        return(json.dumps(user[0].auth_token))

    def generate_zatiq_api_token(self):
        api_token = secrets.token_urlsafe(32)
        if (self.check_api_token_exists(api_token) == False):
            return(api_token)
        else:
            self.generate_zatiq_api_token()

    def check_api_token_exists(self, api_token):
        check_api_token = Zatiq_Users.objects(zatiq_token=api_token)
        if len(check_api_token) > 0:
            self.generate_zatiq_api_token()
        else:
            return(False)
    
    def check_user_exists(self, id, user_email, method, authToken):
        if method == "google":
            check_user_exists = Zatiq_Users.objects(google_id=id, user_email=user_email)
            if len(check_user_exists) > 0:
                update_user_auth_token = Zatiq_Users.objects(google_id=id).update_one(upsert=True, set__auth_token=authToken)
                return(True)
            else:
                return(False)

        if method == 'facebook':
            check_user_exists = Zatiq_Users.objects(facebook_id=id, user_email=user_email)
            if len(check_user_exists) > 0:
                update_user_auth_token = Zatiq_Users.objects(facebook_id=id).update_one(upsert=True, set__auth_token=authToken)
                return(True)
            else:
                return(False)
        
        if method != 'google' and method != 'facebook':
            return(False)
        
    def get_user_info(self, authToken, method):
        if method == 'facebook':
            user_info = requests.get('https://graph.facebook.com/me?fields=name,email&access_token='+authToken)
            return(user_info.json())

        if method == 'google':
            user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+authToken)
            return(user_info.json())
        
        if method != 'google' and method != 'facebook':
            return('Could not authenticate')
    
    def user_login(self, authToken, userEmail, method):
        if not authToken:
            return('Could not authenticate')
        if not userEmail:
            return('Could not authenticate')

        check_user_login = Zatiq_Users.objects(auth_token=authToken)

        if len(check_user_login) > 0:
            user_info = self.get_user_info(authToken, method)
            user_name = user_info['name']
            user_email = user_info['email']
            api_token = check_user_login[0].zatiq_token
            return(json.dumps([user_name, user_email, api_token]))
        else:
            return('Could not authenticate')
        
    def user_register(self, authToken, method):
        if not authToken:
            return('Could not authenticate')
        
        check_user_register = Zatiq_Users.objects(auth_token=authToken)
        if len(check_user_register) > 0:
            return(self.user_login(authToken, check_user_register[0].user_email, method))
        else:
            user_info = self.get_user_info(authToken, method)
            user_id = user_info['id']
            user_email = user_info['email']
            user_name = user_info['name']
            api_token = self.generate_zatiq_api_token()

            if method == 'google':
                if self.check_user_exists(user_email, user_id, method, authToken) == False:
                    user_register = Zatiq_Users.objects(auth_token=authToken).update_one(upsert=True, set__user_email=user_email, set__user_name=user_name, set__google_id=user_id, set__zatiq_token=api_token)
                    return(self.user_login(authToken, user_email, method))
                else:
                    return(self.user_login(authToken, user_email, method))

            if method == 'facebook':
                if self.check_user_exists(user_email, user_id, method, authToken) == False:
                    user_register = Zatiq_Users.objects(auth_token=authToken).update_one(upsert=True, set__user_email=user_email, set__user_name=user_name, set__facebook_id=user_id, set__zatiq_token=api_token)
                    return(self.user_login(authToken, user_email, method))
                else:
                    return(self.user_login(authToken, user_email, method))