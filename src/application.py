from flask import Flask, request, make_response, jsonify
from zatiq_users_mongodb_client import ZatiqUsersMongoDBClient
from zatiq_businesses_mongodb_client import ZatiqBusinessesMongoDBClient
from zatiq_reviews_mongodb_client import ZatiqReviewsMongoDBClient
from zatiq_food_items_mongodb_client import ZatiqFoodItemsMongoDBClient
from requests import post
import logging
from mongoengine import *

application = Flask(__name__)
connect('zatiq_database', host='165.227.43.65', username='zatiqadmin', password='zatiqserver')
#connect('zatiq_database', username='zatiqadmin', password='zatiqserver')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='./app.log', filemode='w')

timely_meals = ['breakfast', 'brunch', 'lunch', 'dinner']
cuisine_types = ['canadian', 'caribbean', 'chinese', 'dessert', 'fast_food', 'fine_food', 'gluten_free', 'greek', 'halal', 'healthy',
    'indian', 'italian', 'japanese', 'korean', 'kosher', 'mexican', 'middle_eastern', 'pizza', 'quick_bite', 'spicy', 'sushi', 'thai',
    'vegan', 'vegetarian', 'vietnamese']
buttons = ['top_picks', 'surprise_me', 'newest', 'promotions']

@application.route('/')
def hello_world():
    return('Hello World!')

@application.route('/user/login/', methods=['POST'])
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

@application.route('/business/register/', methods=['POST'])
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

@application.route('/business/profile/edit/', methods=['POST'])
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

@application.route('/business/login/', methods=['POST'])
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

@application.route('/business/logout/', methods=['POST'])
def logout_as_business():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_businesses.business_logout(api_token)
        return(jsonify(response=response))

@application.route('/business/profile/', methods=['POST'])
def get_business_profile():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_businesses.get_business_profile(api_token)
        return(jsonify(response=response))

@application.route('/user/review/add/', methods=['POST'])
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

@application.route('/user/reviews/all/', methods=['POST'])
def get_all_reviews_by_user():
    if request.method == 'POST':
        zatiq_reviews = ZatiqReviewsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        self_reviews = zatiq_reviews.get_all_reviews_by_reviewer_id(api_token)
        return(jsonify(reviews=self_reviews))

@application.route('/business/reviews/all/', methods=['POST'])
def get_all_reviews_for_business():
    if request.method == 'POST':
        zatiq_business_reviews = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        business_reviews = zatiq_business_reviews.get_all_reviews(api_token)
        return(jsonify(reviews=business_reviews))

@application.route('/business/add/food/', methods=['POST'])
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

@application.route('/restaurant/menu/add/', methods=['POST'])
def add_menu_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image = jsonData['base64']
        image_aspect_ratio = jsonData['image_aspect_ratio']
        add_menu = zatiq_businesses.upload_menu_photo(image, image_aspect_ratio, api_token)
        return(jsonify(response=add_menu))

@application.route('/restaurant/menu/delete/', methods=['POST'])
def delete_menu_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image_id = jsonData['image_id']
        delete_menu = zatiq_businesses.delete_menu_photo(image_id, api_token)
        return(jsonify(response=delete_menu))

@application.route('/restaurant/interior/add/', methods=['POST'])
def add_interior_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image = jsonData['base64']
        image_aspect_ratio = jsonData['image_aspect_ratio']
        add_menu = zatiq_businesses.upload_interior_photo(image, image_aspect_ratio, api_token)
        return(jsonify(response=add_menu))

@application.route('/restaurant/interior/delete/', methods=['POST'])
def delete_interior_photo():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        image_id = jsonData['image_id']
        delete_interior = zatiq_businesses.delete_interior_photo(image_id, api_token)
        return(jsonify(response=delete_interior))

@application.route('/restaurant/menu/all/', methods=['POST'])
def get_menus_for_restaurant():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        menu_photos = zatiq_businesses.get_menu_photos_by_restaurant(api_token)
        return(jsonify(menu_photos=menu_photos))

@application.route('/restaurant/interior/all/', methods=['POST'])
def get_interiors_for_restaurant():
    if request.method == 'POST':
        zatiq_businesses = ZatiqBusinessesMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        interior_photos = zatiq_businesses.get_interior_photos_by_restaurant(api_token)
        return(jsonify(interior_photos=interior_photos))

@application.route('/food/id/', methods=['POST'])
def get_food_item_by_id():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        food_item_id = jsonData['food_item_id']
        food_item = zatiq_food_items.get_food_by_id(api_token, food_item_id)
        return(jsonify(food_item=food_item))

@application.route('/food/restaurantid/', methods=['POST'])
def get_food_items_by_restaurant_id():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        if 'restaurant_id' in jsonData:
            restaurant_id = jsonData['restaurant_id']
        else:
            restaurant_id = None
        food_items = zatiq_food_items.get_food_items_by_restaurant_id(api_token, restaurant_id)
        return(jsonify(food_items=food_items))

@application.route('/business/edit/food/', methods=['POST'])
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
        calories = jsonData['calories']
        meal_type = jsonData['meal_type']
        item_price = jsonData['item_price']
        response = zatiq_food_items.update_food_item(api_token, food_item_id, image, overview, item_name, meal_type, tags, item_price, meat, seafood, calories)
        return(jsonify(response=response[0], food_item_id=response[1]))

@application.route('/user/preferences/', methods=['POST'])
def update_user_preferences():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        user_preferences = jsonData['preferences']
        response = zatiq_users.update_user_preferences(api_token, user_preferences)
        return(jsonify(user_email=response[0], auth_token=response[1], user_name=response[2], preferences=response[3]))

@application.route('/business/delete/food/', methods=['POST'])
def delete_food_item():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        food_item_id = jsonData['food_item_id']
        api_token = jsonData['api_token']
        response = zatiq_food_items.delete_food_item(api_token, food_item_id)
        return(jsonify(response=response))

@application.route('/search/<cuisine_type>/', methods=['POST'])
def search_food_items_by_cuisine_type(cuisine_type):
    if request.method == 'POST':
        zatiq_food_items = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
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
            return('Could not find that category')

@application.route('/user/profile/', methods=['POST'])
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

@application.route('/user/menu/all/', methods=['POST'])
def get_restaurant_menu():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        restaurant_id = jsonData['restaurant_id']
        response = zatiq_users.get_menu_pictures(api_token, restaurant_id)
        return(jsonify(response=response))

@application.route('/user/interior/all/', methods=['POST'])
def get_restaurant_interior():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        restaurant_id = jsonData['restaurant_id']
        response = zatiq_users.get_interior_pictures(api_token, restaurant_id)
        return(jsonify(response=response))

@application.route('/find/restaurant/name/', methods=['POST'])
def get_restaurant_by_name():
    if request.method == 'POST':
        zatiq_users = ZatiqUsersMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        text = jsonData['text']
        response = zatiq_users.get_restaurant_by_name(api_token, text)
        return(jsonify(response=response))

@application.route('/food/grid/', methods=['POST'])
def get_food_grid():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        response = zatiq_food_items.find_food_grid(api_token)
        return(jsonify(food_items=response))

@application.route('/food/grid/name/', methods=['POST'])
def get_food_grid_by_name():
    if request.method == 'POST':
        zatiq_food_items = ZatiqFoodItemsMongoDBClient()
        jsonData = request.get_json()
        api_token = jsonData['api_token']
        text = jsonData['text']
        response = zatiq_food_items.find_food_grid_by_name(api_token, text)
        return(jsonify(response=response))

@application.route('/restaurants/nearby/', methods=['POST'])
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
