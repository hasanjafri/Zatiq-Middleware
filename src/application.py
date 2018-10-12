from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS
import logging
import os
import base64
from logging.handlers import RotatingFileHandler
from logging import getLogger
from config import admin_username, admin_password
from zatiq_users_mongodb_client import ZatiqUsersMongoDBClient
from zatiq_businesses_mongodb_client import ZatiqBusinessesMongoDBClient
from zatiq_reviews_mongodb_client import ZatiqReviewsMongoDBClient
from zatiq_food_items_mongodb_client import ZatiqFoodItemsMongoDBClient
from zatiq_guests_client import ZatiqGuestsClient
from zatiq_deal_items_mongodb_client import ZatiqDealsMongoDBClient
from requests import post
from mongoengine import *
import requests

# logger = logging.getLogger(__name__)
# formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# logger.setLevel(logging.DEBUG)
# handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024, backupCount=5)
# handler.setFormatter(formatter)

application = Flask(__name__)
# application.logger.addHandler(handler)
application.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
application.config['CORS_HEADERS'] = ['Content-Type', 'Authorization']
# connect('zatiq_database', host='165.227.43.65', username='zatiqadmin', password='zatiqserver')
CORS(application, resources={r"/*/*/*": {"origins": "*"}})
connect('zatiq_database', username='zatiqadmin', password='zatiqserver')

timely_meals = ['breakfast', 'brunch', 'lunch', 'dinner']
cuisine_types = ['canadian', 'caribbean', 'chinese', 'dessert', 'fast_food', 'fine_food', 'gluten_free', 'greek', 'halal', 'healthy',
    'indian', 'italian', 'japanese', 'korean', 'kosher', 'mexican', 'middle_eastern', 'pizza', 'quick_bite', 'spicy', 'sushi', 'thai',
    'vegan', 'vegetarian', 'vietnamese']
buttons = ['top_picks', 'surprise_me', 'newest', 'promotions']

ALLOWED_EXTENSIONS = set(['zip'])

@application.route('/api/post', methods=['POST'])
def test_post_cors():
    data = request.get_json()
    return jsonify(data=data)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@application.route('/admin/add/deals', methods=['GET', 'POST'])
def add_zatiq_deal():
    zatiq_deals_client = ZatiqDealsMongoDBClient()
    error = None
    response = None
    food_items_names_dict = zatiq_deals_client.get_list_of_food_items()
    if request.method == 'POST':
        # if 'imagedata' not in request.files:
        #     error = "No image in request.files"
        if 'food' not in request.form:
            error = "No food item selected to link this deal to"
        if 'username' not in request.form:
            error = "Please enter the admin username (Get it from the dev team)"
        if 'password' not in request.form:
            error = "Please enter the admin password"

        username = request.form.get('username')
        password = request.form.get('password')

        if username == admin_username and password == admin_password:   
            # file = request.files['imagedata']
            food_item_id = request.form.get('food')

            # if file.filename == '':
            #     error = "No image file was selected"

            # if file and allowed_file(file.filename):
            # b64_img = base64.b64encode(file.read())
            res = zatiq_deals_client.save_deal_to_db(food_item_id)
            if isinstance(res, dict):
                response = res
            else:
                error = res
        else:
            error = "Invalid admin credentials!"
            
    return render_template('addDeal.html', error=error, response=response, food_items=food_items_names_dict)

@application.route('/admin/upload/AR', methods=['GET'])
def upload_ar_model():
    # error = None
    # response = None
    # if request.method == 'POST':
    #     if 'username' not in request.form:
    #         error = "Please enter the admin username (Get it from the dev team)"
    #     if 'password' not in request.form:
    #         error = "Please enter the admin password"
    #     if 'file' not in request.files:
    #         error = "Error! No zip file attached to upload"

    #     username = request.form.get('username')
    #     password = request.form.get('password')

    #     files_zip = request.files['file']
    #     if files_zip.filename == '':
    #         error = "Error! No zip file was selected!"

    #     if username == admin_username and password == admin_password:
    #         if files_zip and allowed_file(files_zip.filename):
    #             files = {'ar_model_zip': files_zip.read()}
    #             res = requests.post("http://138.197.147.82:8000/upload/", files=files)
    #             if res.status_code == 200:
    #                 response = res
    #             else:
    #                 error = res
    #     else:
    #         error = "Invalid admin credentials!"

    return render_template('uploadARZip.html')

@application.route('/admin/delete/deals', methods=['GET', 'POST'])
def delete_zatiq_deal():
    zatiq_deals_client = ZatiqDealsMongoDBClient()
    error = None
    response = None
    removable_items = zatiq_deals_client.get_organized_remove_deals()
    if request.method == 'POST':
        if 'deal' not in request.form:
            error = "No food_item_id in request"
        if 'username' not in request.form:
            error = "Please enter the admin username (Get it from the dev team)"
        if 'password' not in request.form:
            error = "Please enter the admin password"

        username = request.form.get('username')
        password = request.form.get('password')

        if username == admin_username and password == admin_password:
            food_item_id = request.form.get('deal')
            res = zatiq_deals_client.delete_deal_from_db(food_item_id)
            if isinstance(res, dict):
                response = res
            else:
                error = res
        else:
            error = "Invalid admin credentials!"

    return render_template('removeDeal.html', error=error, response=response, food_items=removable_items)

@application.route('/')
def hello_world():
    return('Hello World!')

@application.route('/deals', methods=['GET'])
def get_all_zatiq_deals():
    if request.method == 'GET':
        zatiq_deals = ZatiqDealsMongoDBClient()
        response = zatiq_deals.get_all_deals()
        return(jsonify(deals=response))

@application.route('/user/login', methods=['POST'])
def login_as_user():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        print(jsonData)
        user_auth_token = jsonData['accessToken']
        user_email = jsonData['email']
        login_method = jsonData['method']
        response = zatiq_users.user_register(user_auth_token, login_method, user_email)
        return(jsonify(user_name=response[0], user_email=response[1], api_token=response[2]))

@application.route('/business/register', methods=['POST'])
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

@application.route('/business/profile/edit', methods=['POST'])
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
        if len(image) < 100:
            response = zatiq_businesses.update_business_profile_without_image(api_token, hours, name, address, website, number, image_aspect_ratio, features)
        else:
            response = zatiq_businesses.update_business_profile_with_image(api_token, hours, name, address, website, number, image, image_aspect_ratio, features)
        return(jsonify(name=response[0], image=response[1], image_aspect_ratio=response[2], api_token=response[3]))  

@application.route('/business/login', methods=['POST'])
def login_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        business_email = jsonData['email']
        business_password = jsonData['password']
        response = zatiq_businesses.business_login(business_email, business_password)
        if len(response) > 1:
            return(jsonify(name=response[0], api_token=response[1], image=response[2], image_aspect_ratio=response[3]))
        else:
            return(jsonify(response=response[0]), 401)

@application.route('/business/logout', methods=['POST'])
def logout_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_businesses.business_logout(api_token)
        return(jsonify(response=response))

@application.route('/business/profile', methods=['POST'])
def get_business_profile():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_businesses.get_business_profile(api_token)
        return(jsonify(response=response))

@application.route('/user/review/add', methods=['POST'])
def add_review_as_user():
    if request.method == 'POST':
        zatiq_reviews = ZatiqReviewsMongoDBClient()
        jsonData = request.get_json()
        restaurant_id = jsonData['restaurant_id']
        food_item_id = jsonData['food_item_id']
        text = jsonData['text']
        rating = jsonData['rating']
        api_token = jsonData['api_token']

        if 'image' in jsonData:
            image = jsonData['image']['base64']
            image_aspect_ratio = jsonData['image']['image_aspect_ratio']
            image_url = post("http://167.99.177.29:5000/upload/", json={'imagedata': image})
            if 'Error' in image_url:
                return("Invalid image provided")
        else:
            image = None
            image_aspect_ratio = None
            
        add_review = zatiq_reviews.add_review(restaurant_id, food_item_id, text, image_url.text, rating, image_aspect_ratio, api_token)
        return(jsonify(response=add_review))

@application.route('/user/reviews/all', methods=['POST'])
def get_all_reviews_by_user():
    if request.method == 'POST':
        zatiq_reviews = ZatiqReviewsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        self_reviews = zatiq_reviews.get_all_reviews_by_reviewer_id(api_token)
        return(jsonify(reviews=self_reviews))

@application.route('/business/reviews/all', methods=['POST'])
def get_all_reviews_for_business():
    if request.method == 'POST':
        zatiq_business_reviews = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        business_reviews = zatiq_business_reviews.get_all_reviews(api_token)
        return(jsonify(reviews=business_reviews))

@application.route('/business/add/food', methods=['POST'])
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
        calories = jsonData['calories']
        seafood = jsonData['seafood']
        meal_type = jsonData['meal_type']
        item_price = jsonData['item_price']
        response = zatiq_food_items.add_food_item(image, overview, item_name, api_token, meal_type, tags, item_price, meat, seafood, calories)
        return(jsonify(response=response))

@application.route('/restaurant/menu/add', methods=['POST'])
def add_menu_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image = jsonData['base64']
        image_aspect_ratio = jsonData['image_aspect_ratio']
        add_menu = zatiq_businesses.upload_menu_photo(image, image_aspect_ratio, api_token)
        return(jsonify(response=add_menu))

@application.route('/restaurant/menu/delete', methods=['POST'])
def delete_menu_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image_id = jsonData['image_id']
        delete_menu = zatiq_businesses.delete_menu_photo(image_id, api_token)
        return(jsonify(response=delete_menu))

@application.route('/restaurant/interior/add', methods=['POST'])
def add_interior_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image = jsonData['base64']
        image_aspect_ratio = jsonData['image_aspect_ratio']
        add_menu = zatiq_businesses.upload_interior_photo(image, image_aspect_ratio, api_token)
        return(jsonify(response=add_menu))

@application.route('/restaurant/interior/delete', methods=['POST'])
def delete_interior_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image_id = jsonData['image_id']
        delete_interior = zatiq_businesses.delete_interior_photo(image_id, api_token)
        return(jsonify(response=delete_interior))

@application.route('/restaurant/menu/all', methods=['POST'])
def get_menus_for_restaurant():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        menu_photos = zatiq_businesses.get_menu_photos_by_restaurant(api_token)
        return(jsonify(menu_photos=menu_photos))

@application.route('/restaurant/interior/all', methods=['POST'])
def get_interiors_for_restaurant():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        interior_photos = zatiq_businesses.get_interior_photos_by_restaurant(api_token)
        return(jsonify(interior_photos=interior_photos))

@application.route('/food/id', methods=['POST'])
def get_food_item_by_id():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        food_item_id = jsonData['food_item_id']
        food_item = zatiq_food_items.get_food_by_id(food_item_id)
        return(jsonify(food_item=food_item))

@application.route('/food/restaurantid', methods=['POST'])
def get_food_items_by_restaurant_id():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        if 'api_token' in jsonData:
            api_token = jsonData['api_token']
        else:
            api_token = None
        if 'restaurant_id' in jsonData:
            restaurant_id = jsonData['restaurant_id']
        else:
            restaurant_id = None
        food_items = zatiq_food_items.get_food_items_by_restaurant_id(api_token, restaurant_id)
        return(jsonify(food_items=food_items))

@application.route('/business/edit/food', methods=['POST'])
def edit_food_item():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        food_item_id = jsonData['food_item_id']
        api_token = jsonData['api_token']
        image = jsonData['image']
        logging.debug(image)
        overview = jsonData['overview']
        item_name = jsonData['item_name']
        tags = jsonData['tags']
        meat = jsonData['meat']
        seafood = jsonData['seafood']
        calories = jsonData['calories']
        meal_type = jsonData['meal_type']
        item_price = jsonData['item_price']
        if len(image) < 100:
            response = zatiq_food_items.update_food_item_without_image(api_token, food_item_id, overview, item_name, meal_type, tags, item_price, meat, seafood, calories)
        else:
            response = zatiq_food_items.update_food_item_with_image(api_token, food_item_id, image, overview, item_name, meal_type, tags, item_price, meat, seafood, calories)
        return(jsonify(response=response[0], food_item_id=response[1]))

@application.route('/user/preferences', methods=['POST'])
def update_user_preferences():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        user_preferences = jsonData['preferences']
        response = zatiq_users.update_user_preferences(api_token, user_preferences)
        return(jsonify(user_email=response[0], auth_token=response[1], user_name=response[2], preferences=response[3]))

@application.route('/business/delete/food', methods=['POST'])
def delete_food_item():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        food_item_id = jsonData['food_item_id']
        api_token = jsonData['api_token']
        response = zatiq_food_items.delete_food_item(api_token, food_item_id)
        return(jsonify(response=response))

@application.route('/search/<cuisine_type>', methods=['POST'])
def search_food_items_by_cuisine_type(cuisine_type):
        zatiq_food_items = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        print(jsonData)
        if 'api_token' not in jsonData:
            return {"error":"Error! No api_token in request.body"}
        else:
            api_token = jsonData['api_token']
        cuisine_type = cuisine_type.replace(' ', '_').lower()
        if cuisine_type in timely_meals:
            zatiq_food_items = ZatiqFoodItemsMongoDBClient()
            response = zatiq_food_items.get_food_items_by_time_of_day(api_token, cuisine_type)
            return(jsonify(food_items=response))
        elif cuisine_type in cuisine_types:
            zatiq_food_items = ZatiqFoodItemsMongoDBClient()
            response = zatiq_food_items.get_food_items_by_cuisine_type(api_token, cuisine_type)
            return(jsonify(food_items=response))
        elif cuisine_type in buttons:
            zatiq_food_items = ZatiqFoodItemsMongoDBClient()
            response = zatiq_food_items.get_food_items_by_button(api_token, cuisine_type)
            return(jsonify(food_items=response))
        else:
            return {"error":"Error! Could not find that category"}

@application.route('/guest/<tag>', methods=['GET'])
def get_guest_items(tag):
    if request.method == 'GET':
        zatiq_guests = ZatiqGuestsClient()
        tag = tag.replace(' ', '_').lower()

        if tag in buttons:
            response = zatiq_guests.get_guest_food_by_button(tag)
            return(jsonify(food_items=response))
        else:
            return('Could not find that category')

@application.route('/user/profile', methods=['POST'])
def get_user_profile():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_users.get_user_profile(api_token)
        if len(response) == 4:
            return(jsonify(user_email=response[0], auth_token=response[1], user_name=response[2], preferences=response[3]))
        elif len(response) == 3:
            return(jsonify(user_email=response[0], user_name=response[1], preferences=response[2]))
        else:
            return(jsonify(response=response))

@application.route('/user/menu/all', methods=['POST'])
def get_restaurant_menu():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        restaurant_id = jsonData['restaurant_id']
        response = zatiq_users.get_menu_pictures(restaurant_id)
        return(jsonify(response=response))

@application.route('/user/interior/all', methods=['POST'])
def get_restaurant_interior():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        restaurant_id = jsonData['restaurant_id']
        response = zatiq_users.get_interior_pictures(restaurant_id)
        return(jsonify(response=response))

@application.route('/find/restaurant/name', methods=['POST'])
def get_restaurant_by_name():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        text = jsonData['text']
        response = zatiq_users.get_restaurant_by_name(api_token, text)
        return(jsonify(response=response))

@application.route('/food/grid', methods=['POST'])
def get_food_grid():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_food_items.find_food_grid(api_token)
        return(jsonify(food_items=response))

@application.route('/food/grid/name', methods=['POST'])
def get_food_grid_by_name():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        text = jsonData['text']
        response = zatiq_food_items.find_food_grid_by_name(api_token, text)
        return(jsonify(response=response))

@application.route('/restaurants/nearby', methods=['POST'])
def get_nearby_restaurants():
    if request.method == 'POST':
        zatiq_restaurants = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_restaurants.get_nearby_restaurants(api_token)
        return(jsonify(response=response))

if __name__ == "__main__":
    application.debug = True
    application.run(host='0.0.0.0')
