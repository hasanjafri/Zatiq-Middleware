from flask import Flask, request, make_response, jsonify
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
        return(jsonify(user_name=response[0], user_email=response[1], api_token=response[2]))

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
        hours = jsonData['date']
        name = jsonData['name']
        address = jsonData['address']
        website = jsonData['website']
        number = jsonData['number']
        image = jsonData['image']['base64']
        image_aspect_ratio = jsonData['image']['image_aspect_ratio']
        features = jsonData['features']
        response = zatiq_businesses.business_register(business_email, business_password, hours, name, address, website, number, image, image_aspect_ratio, features)
        return(jsonify(name=response[0], api_token=response[1], image=response[2], image_aspect_ratio=response[3]))

@app.route('/business/profile/edit/', methods=['POST'])
def edit_business_profile():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        hours = jsonData['date']
        name = jsonData['name']
        address = jsonData['address']
        website = jsonData['website']
        number = jsonData['number']
        image = jsonData['image']['base64']
        image_aspect_ratio = jsonData['image']['image_aspect_ratio']
        features = jsonData['features']
        response = zatiq_businesses.update_business_profile(api_token, hours, name, address, website, number, image, image_aspect_ratio, features)
        return(jsonify(name=response[0], image=response[1], image_aspect_ratio=response[2], api_token=response[3]))  

@app.route('/business/login/', methods=['POST'])
def login_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        business_email = jsonData['email']
        business_password = jsonData['password']
        response = zatiq_businesses.business_login(business_email, business_password)
        return(jsonify(name=response[0], api_token=response[1], image=response[2], image_aspect_ratio=response[3]))

@app.route('/business/logout/', methods=['POST'])
def logout_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_businesses.business_logout(api_token)
        return(jsonify(response=response))

@app.route('/business/profile/', methods=['POST'])
def get_business_profile():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_businesses.get_business_profile(api_token)
        return(jsonify(email=response[0], name=response[1], website=response[2], address=response[3], number=response[4], image=response[5], api_token=response[6], hours=response[7], delivery=response[8], takeout=response[9], reservation=response[10], patio=response[11], wheelchair_accessible=response[12]))

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
        api_token = jsonData['api_token']
        image = jsonData['image']
        overview = jsonData['overview']
        item_name = jsonData['item_name']
        tags = jsonData['tags']
        meat = jsonData['meat']
        seafood = jsonData['seafood']
        meal_type = jsonData['meal_type']
        item_price = jsonData['item_price']
        response = zatiq_food_items.add_food_item(image, overview, item_name, api_token, meal_type, tags, item_price, meat, seafood)
        return(jsonify(response=response))

@app.route('/food/cuisine/', methods=['POST'])
def query_food_items_by_cuisine():
    if request.method == 'POST':
        pass

@app.route('/restaurant/menu/add/', methods=['POST'])
def add_menu_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image = jsonData['base64']
        image_aspect_ratio = jsonData['image_aspect_ratio']
        add_menu = zatiq_businesses.upload_menu_photo(image, image_aspect_ratio, api_token)
        return(jsonify(response=add_menu))

@app.route('/restaurant/menu/delete/', methods=['POST'])
def delete_menu_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image_id = jsonData['image_id']
        delete_menu = zatiq_businesses.delete_menu_photo(image_id, api_token)
        return(jsonify(response=delete_menu))

@app.route('/restaurant/interior/add/', methods=['POST'])
def add_interior_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image = jsonData['base64']
        image_aspect_ratio = jsonData['image_aspect_ratio']
        add_menu = zatiq_businesses.upload_interior_photo(image, image_aspect_ratio, api_token)
        return(jsonify(response=add_menu))

@app.route('/restaurant/interior/delete/', methods=['POST'])
def delete_interior_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image_id = jsonData['image_id']
        delete_interior = zatiq_businesses.delete_interior_photo(image_id, api_token)
        return(jsonify(response=delete_interior))

@app.route('/restaurant/menu/all/', methods=['POST'])
def get_menus_for_restaurant():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        menu_photos = zatiq_businesses.get_menu_photos_by_restaurant(api_token)
        return(jsonify(menu_photos=menu_photos))

@app.route('/restaurant/interior/all/', methods=['POST'])
def get_interiors_for_restaurant():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        interior_photos = zatiq_businesses.get_interior_photos_by_restaurant(api_token)
        return(jsonify(interior_photos=interior_photos))

@app.route('/food/id/', methods=['POST'])
def get_food_item_by_id():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        food_item_id = jsonData['food_item_id']
        food_item = zatiq_food_items.get_food_by_id(api_token, food_item_id)
        return(jsonify(food_item=food_item))

@app.route('/food/restaurantid/', methods=['POST'])
def get_food_items_by_restaurant_id():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        food_items = zatiq_food_items.get_food_items_by_restaurant_id(api_token)
        return(jsonify(food_items=food_items))

@app.route('/business/edit/food/', methods=['POST'])
def edit_food_item():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        food_item_id = jsonData['food_item_id']
        api_token = jsonData['api_token']
        image = jsonData['image']
        overview = jsonData['overview']
        item_name = jsonData['item_name']
        tags = jsonData['tags']
        meat = jsonData['meat']
        seafood = jsonData['seafood']
        meal_type = jsonData['meal_type']
        item_price = jsonData['item_price']
        response = zatiq_food_items.update_food_item(api_token, food_item_id, image, overview, item_name, meal_type, tags, item_price, meat, seafood)
        return(jsonify(response=response))

@app.route('/user/preferences/', methods=['POST'])
def update_user_preferences():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        user_preferences = jsonData['preferences']
        pass

@app.route('/business/delete/food/', methods=['POST'])
def delete_food_item():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        food_item_id = jsonData['food_item_id']
        api_token = jsonData['api_token']
        response = zatiq_food_items.delete_food_item(api_token, food_item_id)
        return(jsonify(response=response))


