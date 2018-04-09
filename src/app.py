from flask import Flask, request
from zatiq_users_mongodb_client import ZatiqUsersMongoDBClient
from zatiq_businesses_mongodb_client import ZatiqBusinessesMongoDBClient
from zatiq_reviews_mongodb_client import ZatiqReviewsMongoDBClient
from mongoengine import *

app = Flask(__name__)
connect('zatiq_database')

@app.route('/')
def hello_world():
    return('Hello World!')

@app.route('/user/login/', methods=['POST'])
def login_as_user():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        user_auth_token = jsonData['accessToken']
        login_method = jsonData['method']
        response = zatiq_users.user_register(user_auth_token, login_method)
        return(response)

@app.route('/users/list/')
def test_get_all_users():
    all_users = ZatiqUsersMongoDBClient().get_all_users()
    return(all_users)

@app.route('/user/')
def test_get_specific_user():
    api_token = request.get_json()['api_token']
    user = ZatiqUsersMongoDBClient().get_specific_user(api_token)
    return(user)

@app.route('/business/login/', methods=['POST'])
def login_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        business_email = jsonData['email']
        business_password = jsonData['password']
        response = zatiq_businesses.business_register(business_email, business_password)
        return(response)

@app.route('/user/review/add/', methods=['POST'])
def add_review_as_user():
    if request.method == 'POST':
        
