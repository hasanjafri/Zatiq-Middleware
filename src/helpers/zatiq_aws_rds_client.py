import MySQLdb

class ZatiqAWSRDSClient(object):
    def __init__(self):
        self.connect_to_rds = MySQLdb.connect(
            
        )
    
    def get_all_businesses(self):
        db_query = self.connect_to_rds.cursor()
        db_query.execute("""SELECT * from ZatiqBusinesses""")
        response = db_query.fetchall()
        print(response)
        return("Done!")

    def business_login(self, businessEmail, businessPassword):
        if not businessEmail:
            return("Please specify your email!")
        if not businessPassword:
            return("Please type your password!")
        
        db_query = self.connect_to_rds.cursor()
        db_query.execute("""SELECT * FROM ZatiqBusinesses WHERE businessEmail = %s AND businessPassword = %s""", (businessEmail, businessPassword))

        res = db_query.fetchall()

        if len(res) > 0:
            logged_in_business = res[0][1]
            has_set_information = res[0][4]
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
        
        db_query = self.connect_to_rds.cursor()
        db_query.execute("""SELECT * FROM ZatiqBusinesses WHERE businessEmail = %s""", [businessEmail])

        res = db_query.fetchall()

        if len(res) > 0:
            return("Business is already registered with this email")
        else:
            register_query = self.connect_to_rds.cursor()
            #businessInfo = {"businessName": businessName, "businessEmail": businessEmail, "businessPassword": businessPassword}
            register_query.execute("""INSERT INTO ZatiqBusinesses (businessName, businessEmail, businessPassword) VALUES (%s, %s, %s)""", (businessName, businessEmail, businessPassword))
            print(register_query.fetchall())

        
