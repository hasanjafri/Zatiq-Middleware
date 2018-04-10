from flask import Flask, request, make_response
from zatiq_users_mongodb_client import ZatiqUsersMongoDBClient
from zatiq_businesses_mongodb_client import ZatiqBusinessesMongoDBClient
from zatiq_reviews_mongodb_client import ZatiqReviewsMongoDBClient
from zatiq_food_items_mongodb_client import ZatiqFoodItemsMongoDBClient
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

@app.route('/business/register/', methods=['POST'])
def register_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        business_email = jsonData['email']
        business_password = jsonData['password']
        response = zatiq_businesses.business_register(business_email, business_password)
        json_resp = make_response(response, 200)
        json_resp.mimetype = 'application/json'
        return(json_resp)

@app.route('/business/login/', methods=['POST'])
def login_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        business_email = jsonData['email']
        business_password = jsonData['password']
        response = zatiq_businesses.business_login(business_email, business_password)
        return(response)

@app.route('/reviews/all/user/', methods=['POST'])
def get_all_reviews_by_reviewer_id():
    if request.method == 'POST':
        api_token = request.get_json()['api_token']


@app.route('/user/review/add/', methods=['POST'])
def add_review_as_user():
    if request.method == 'POST':
        zatiq_reviews = ZatiqReviewsMongoDBClient()
        jsonData = request.get_json()
        restaurant_id = jsonData['restaurant_id']
        reviewer_id = jsonData['reviewer_id']
        food_item_id = jsonData['food_item_id']
        text = jsonData['text']
        rating = jsonData['rating']
        api_token = jsonData['api_token']

        if jsonData['image']:
            image = jsonData['image']
            image_aspect_ratio = jsonData['image_aspect_ratio']
        else:
            image = None
            image_aspect_ratio = None
            
        all_reviews_by_restaurantid = zatiq_reviews.add_review(restaurant_id, reviewer_id, food_item_id, text, image, rating, image_aspect_ratio, api_token)
        return(all_reviews_by_restaurantid)

@app.route('/business/add/food/', methods=['POST'])
def add_food_item_as_business():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        restaurant_id = jsonData['restaurant_id']
        image = jsonData['image']
        image_aspect_ratio = jsonData['image_aspect_ratio']
        overview = jsonData['overview']
        item_name = jsonData['item_name']
        foods_by_current_restaurant_id = zatiq_food_items.add_food_item(restaurant_id, image, image_aspect_ratio, overview, item_name)
        return(foods_by_current_restaurant_id)
