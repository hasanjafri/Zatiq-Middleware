from mongoengine import *
import secrets
import json
from simplecrypt import encrypt, decrypt
from config import secret
from zatiq_businesses import Zatiq_Businesses

class ZatiqBusinessesMongoDBClient(object):
    def get_all_businesses(self):
        all_businesses = []
        for user in Zatiq_Businesses.objects:
            all_businesses.append(user.user_name)
        return(json.dumps(all_businesses))

    def get_specific_business(self, businessEmail):
        business = Zatiq_Businesses.objects(business_email=businessEmail)
        return(json.dumps(business[0].business_name))

    def generate_zatiq_api_token(self):
        api_token = secrets.token_urlsafe(32)
        if (self.check_api_token_exists(api_token) == False):
            return(api_token)
        else:
            self.generate_zatiq_api_token()

    def check_api_token_exists(self, api_token):
        check_api_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if len(check_api_token) > 0:
            self.generate_zatiq_api_token()
        else:
            return(False)

    def encrypt_password(self, password):
        encrypted_password = encrypt(secret, password.encode('utf-8'))
        return(encrypted_password)

    def verify_password(self, password, encrypted_password):
        decrypted_password = decrypt(secret, encrypted_password)
        password_str = decrypted_password.decode('utf-8')
        if password_str == password:
            return(True)
        else:
            return(False)

    def business_login(self, business_email, business_password):
        if not business_email:
            return('Please specify your email!')
        if not business_password:
            return('Please type your password!')

        check_business_login = Zatiq_Businesses.objects(business_email=business_email)

        if len(check_business_login) > 0:
            encrypted_password = check_business_login[0].business_password
            if self.verify_password(business_password, encrypted_password) == True:
                business_name = check_business_login[0].business_name
                business_email = check_business_login[0].business_email
                has_set_information = check_business_login[0].has_set_information
                api_token = check_business_login[0].zatiq_token
                return(json.dumps([business_name, business_email, has_set_information, api_token]))
            else:
                return('Incorrect Password!')
        else:
            return("No such email address!")

    def business_register(self, business_email, business_password):
        if not business_email:
            return("Please specify your email")
        if not business_password:
            return("Please type in your password")

        check_business_register = Zatiq_Businesses.objects(business_email=business_email)
        if len(check_business_register) > 0:
            return("Business is already registered with this email")
        else:
            encrypted_password = self.encrypt_password(business_password)
            api_token = self.generate_zatiq_api_token()
            register_business = Zatiq_Businesses.objects(business_email=business_email).update_one(upsert=True, set__business_password=encrypted_password, set__zatiq_token=api_token)
            return(self.business_login(business_email, business_password))
