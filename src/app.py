from flask import Flask
from zatiq_businesses_mysql_client import ZatiqBusinessesMySQLClient
from zatiq_users_mysql_client import ZatiqUsersMySQLClient
app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello World!')

@app.route('/businesses/list/')
def test_get_first_business():
    zatiq_businesess = ZatiqBusinessesMySQLClient()
    response = zatiq_businesess.get_all_businesses()
    return(response)

@app.route('/users/list/')
def test_get_first_user():
    zatiq_users = ZatiqUsersMySQLClient()
    response = zatiq_users.get_all_users()
    return(response)

# @app.route('/business/login/')
# def business_login():
#     zatiq_rds = ZatiqAWSRDSClient()
#     response = zatiq_rds.business_login("test", "testing")
#     if isinstance(response, str):
#         return(response)
#     else:
#         return('' + response[0] + '\n' + response[1])

# @app.route('/business/register/')
# def business_register():
#     zatiq_rds = ZatiqAWSRDSClient()
#     response = zatiq_rds.business_register("flask", "flask@flask.com", "hasan")
#     #response = zatiq_rds.business_register("test", "test", "test")
#     return("hey")
