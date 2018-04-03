import MySQLdb
import secrets
import requests
import json

class ZatiqUsersMySQLClient(object):
    def __init__(self):
        self.connect_to_db = MySQLdb.connect(
            host="127.0.0.1",
            user="root",
            passwd="zatiqserver",
            db="zatiq_database"
        )
    
    def get_all_users(self):
        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * from zatiq_users""")
        response = db_query.fetchall()
        return(json.dumps(response[0]))
    
    def generate_zatiq_api_token(self):
        api_token = secrets.token_urlsafe(32)
        if self.check_api_token_exists(api_token) == False:
            return(api_token)
        else:
            self.generate_zatiq_api_token()

    def check_api_token_exists(self, api_token):
        check_api_token = self.connect_to_db.cursor()
        check_api_token.execute("""SELECT * FROM zatiq_users WHERE zatiq_token = %s""", [api_token])
        response = check_api_token.fetchall()
        if len(response) > 0:
            self.generate_zatiq_api_token()
        else:
            return(False)

    def get_user_info(self, authToken, method):
        if method == 'facebook':
            user_info = requests.get('https://graph.facebook.com/me?fields=name,email&access_token='+authToken)
            user_info_json = user_info.json()
            return(user_info_json)
        
        if method == 'google':
            user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+authToken)
            user_info_json = user_info.json()
            return(user_info_json)

        if method != 'google' and method != 'facebook':
            return('Could not authenticate')
        

    def user_login(self, authToken, userEmail, method):
        if not authToken:
            return("Could not authenticate")
        if not userEmail:
            return("Could not authenticate")

        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * FROM zatiq_users WHERE auth_token = %s""", [authToken])
        
        response = db_query.fetchall()

        if len(response) > 0:
            user_info = self.get_user_info(authToken, method)
            has_set_preferences = response[0][3]
            user_name = user_info['name']
            user_email = user_info['email']
            api_token = response[0][5]
            return(has_set_preferences, user_name, user_email, api_token)
        else:
            return("Could not authenticate")

    def user_register(self, authToken, method):
        if not authToken:
            return("Could not authenticate")

        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * FROM zatiq_users WHERE auth_token = %s""", [authToken])

        response = db_query.fetchall()
        if len(response) > 0:
            self.user_login(authToken, response[0][1], method)
        else:
            register_user = self.connect_to_db.cursor()
            user_info = self.get_user_info(authToken, method)
            user_id = user_info['id']
            user_email = user_info['email']
            user_name = user_info['name']
            api_token = self.generate_zatiq_api_token()

            if method == 'google':
                register_user.execute("""INSERT INTO zatiq_users (user_email, user_name, auth_token, zatiq_token, google_id) VALUES (%s, %s, %s, %s, %s)""", (
                    user_email, user_name, authToken, api_token, user_id))

            if method == 'facebook':
                register_user.execute("""INSERT INTO zatiq_users (user_email, user_name, auth_token, zatiq_token, facebook_id) VALUES (%s, %s, %s, %s, %s)""", (
                    user_email, user_name, authToken, api_token, user_id))
            
