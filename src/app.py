from flask import Flask, request
from zatiq_users_mongodb_client import ZatiqUsersMongoDBClient
from mongoengine import *

app = Flask(__name__)
connect('zatiq_database')

@app.route('/')
def hello_world():
    return('Hello World!')

# @app.route('/businesses/list/')
# def test_get_first_business():
#     zatiq_businesess = ZatiqBusinessesMySQLClient()
#     response = zatiq_businesess.get_all_businesses()
#     return(response)

# @app.route('/users/list/')
# def test_get_first_user():
#     zatiq_users = ZatiqUsersMySQLClient()
#     response = zatiq_users.get_all_users()
#     return(response)

# @app.route('/user/login/', methods=['POST'])
# def login_as_user():
#     if request.method == 'POST':
#         zatiq_users = ZatiqUsersMySQLClient()
#         jsonData = request.get_json()
#         print(jsonData)
#         user_auth_token = jsonData['accessToken']
#         login_method = jsonData['method']
#         response = zatiq_users.user_register(user_auth_token, login_method)
#         return(response)

@app.route('/users/list/')
def test_get_all_users():
    all_users = ZatiqUsersMongoDBClient().get_all_users()
    return(all_users)

@app.route('/user/')
def test_get_specific_user():
    user = ZatiqUsersMongoDBClient().get_specific_user()
    return(user)
