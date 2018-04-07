import MySQLdb
from simplecrypt import encrypt, decrypt
from config import secret
import json

class ZatiqBusinessesMySQLClient(object):
    def __init__(self):
        self.connect_to_db = MySQLdb.connect(
            host="127.0.0.1",
            user="root",
            passwd="zatiqserver",
            db="zatiq_database"
        )

    def generate_zatiq_api_token(self):
        api_token = secrets.token_urlsafe(32)
        if self.check_api_token_exists(api_token) == False:
            return(api_token)
        else:
            self.generate_zatiq_api_token()

    def check_api_token_exists(self, api_token):
        check_api_token = self.connect_to_db.cursor()
        check_api_token.execute(
            """SELECT * FROM zatiq_users WHERE zatiq_token = %s""", [api_token])
        response = check_api_token.fetchall()
        if len(response) > 0:
            self.generate_zatiq_api_token()
        else:
            return(False)

    def get_all_businesses(self):
        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * from zatiq_businesses""")
        response = db_query.fetchall()
        return(json.dumps(response[0]))

    def encrypt_passwd(self, password):
        encrypted_pwd = encrypt(secret, password.encode('utf-8'))
        return(encrypted_pwd)
    
    def verify_passwd(self, password, encrypted_pwd):
       decrypted_pwd = decrypt(secret, encrypted_pwd)
       pwd_str = decrypted_pwd.decode('utf-8')
       if pwd_str == password:
           return(True)
       else:
           return(False)

    def business_login(self, businessEmail, businessPassword):
        if not businessEmail:
            return("Please specify your email!")
        if not businessPassword:
            return("Please type your password!")

        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * FROM zatiq_businesses WHERE businessEmail = %s""", (businessEmail)

        response = db_query.fetchall()

        if len(response) > 0:
            encrypted_pwd = response[0][2]
            if self.verify_passwd(businessPassword, encrypted_pwd) == True:
                business_name = response[0][3]
                business_email = response[0][1]
                has_set_information = response[0][4]
                return(json.dumps([business_name, business_email, has_set_information]))
            else:
                return("Incorrect Password!")
        else:
            return("No such email address!")

    def business_register(self, businessName, businessEmail, businessPassword):
        if not businessEmail:
            return("Please specify your email")
        if not businessPassword:
            return("Please type in your password")
        if not businessName:
            return("Please type in your Business's Name")

        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * FROM ZatiqBusinesses WHERE businessEmail = %s""", [businessEmail])

        res = db_query.fetchall()

        if len(res) > 0:
            return("Business is already registered with this email")
        else:
            register_business = self.connect_to_db.cursor()
            encrypted_pwd = self.encrypt_passwd(businessPassword)
            api_token = self.generate_zatiq_api_token()
            if register_business.execute("""INSERT INTO zatiq_businesses (business_email, business_password, business_name, zatiq_token) VALUES (%s, %s, %s, %s)""", (businessEmail, encrypted_pwd, businessName, api_token)) == 1:
                self.connect_to_db.commit()
                return(self.business_login(businessEmail, businessPassword))
            else:
                return("An error occurred, please try again!")
