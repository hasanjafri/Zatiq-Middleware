import MySQLdb
from cryptography.fernet import Fernet
from config import secret_key

class ZatiqBusinessesMySQLClient(object):
    def __init__(self):
        self.connect_to_db = MySQLdb.connect(
            host="127.0.0.1",
            user="root",
            passwd="zatiqserver",
            db="zatiq_database"
        )

    def get_all_businesses(self):
        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * from zatiq_businesses""")
        response = db_query.fetchall()
        return(response)

    def encrypt_passwd(self, password):
        encryption = Fernet(secret_key)
        encrypted_pwd = encryption.encrypt(b"" + str(password))
        return(bytes(encrypted_pwd).decode("utf-8"))
    
    def decode_passwd(self, password):
       encryption = Fernet(secret_key)
       encrypted_pwd = password.encode()
       decrypted_pwd = (encryption.decrypt(encrypted_pwd))
       return(bytes(decrypted_pwd).decode("utf-8"))

    def business_login(self, businessEmail, businessPassword):
        if not businessEmail:
            return("Please specify your email!")
        if not businessPassword:
            return("Please type your password!")

        db_query = self.connect_to_db.cursor()
        db_query.execute("""SELECT * FROM zatiq_businesses WHERE businessEmail = %s AND businessPassword = %s""", (businessEmail, businessPassword))

        response = db_query.fetchall()

        if len(response) > 0:
            logged_in_business = response[0][3]
            has_set_information = response[0][4]
            return(logged_in_business, has_set_information)
        else:
            return("No such user!")

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
            register_query = self.connect_to_db.cursor()
            #businessInfo = {"businessName": businessName, "businessEmail": businessEmail, "businessPassword": businessPassword}
            register_query.execute("""INSERT INTO ZatiqBusinesses (businessName, businessEmail, businessPassword) VALUES (%s, %s, %s)""", (
                businessName, businessEmail, businessPassword))
            print(register_query.fetchall())
        
