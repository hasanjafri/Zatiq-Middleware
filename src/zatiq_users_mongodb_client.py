from mongoengine import *
import secrets
import requests
import json
from zatiq_users import Zatiq_Users
from zatiq_food_items import Zatiq_Food_Items

class ZatiqUsersMongoDBClient(object):
    def get_all_users(self):
        all_users = []
        for user in Zatiq_Users.objects:
            all_users.append(user.user_name)
        print(all_users)
        return(json.dumps(all_users))
    
    def get_specific_user(self, api_token):
        user = Zatiq_Users.objects(zatiq_token=api_token)
        return(json.dumps(user[0].auth_token))

    def generate_zatiq_api_token(self):
        api_token = secrets.token_urlsafe(32)
        if (self.check_api_token_exists(api_token) == False):
            return(api_token)
        else:
            self.generate_zatiq_api_token()

    def get_user_id_by_api_token(self, api_token):
        valid_token = Zatiq_Users.objects(zatiq_token=api_token)
        if (len(valid_token) > 0):
            user_id = valid_token[0].id
            return(user_id)
        else:
            return(None)

    def check_valid_api_token(self, api_token):
        valid_token = Zatiq_Users.objects(zatiq_token=api_token)
        if len(valid_token) > 0:
            return(True)
        else:
            return(False)

    def check_api_token_exists(self, api_token):
        check_api_token = Zatiq_Users.objects(zatiq_token=api_token)
        if len(check_api_token) > 0:
            self.generate_zatiq_api_token()
        else:
            return(False)
    
    def check_user_exists(self, id, user_email, method, authToken):
        if method == "google":
            check_user_exists = Zatiq_Users.objects(google_id=id, user_email=user_email)
            if len(check_user_exists) > 0:
                update_user_auth_token = Zatiq_Users.objects(google_id=id).update_one(upsert=True, set__auth_token=authToken)
                return(True)
            else:
                return(False)

        if method == 'facebook':
            check_user_exists = Zatiq_Users.objects(facebook_id=id, user_email=user_email)
            if len(check_user_exists) > 0:
                update_user_auth_token = Zatiq_Users.objects(facebook_id=id).update_one(upsert=True, set__auth_token=authToken)
                return(True)
            else:
                return(False)
        
        if method != 'google' and method != 'facebook':
            return(False)
        
    def get_user_info(self, authToken, method):
        if method == 'facebook':
            user_info = requests.get('https://graph.facebook.com/me?fields=name,email&access_token='+authToken)
            return(user_info.json())

        if method == 'google':
            user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token='+authToken)
            return(user_info.json())
        
        if method != 'google' and method != 'facebook':
            return('Could not authenticate')

    def get_user_profile(self, api_token):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                get_user_info = Zatiq_Users.objects(zatiq_token=api_token)
            except Exception as e:
                return("Error \n %s" % (e))
            user_email = get_user_info[0].user_email
            auth_token = get_user_info[0].auth_token
            user_name = get_user_info[0].user_name
            preferences = self.generate_preferences_dict(get_user_info[0].preferences)
            return([user_email, auth_token, user_name, preferences])

    def generate_preferences_dict(self, preferences):
        preferences_dict = {'halal': preferences.halal, 'spicy': preferences.spicy, 'kosher': preferences.kosher, 'healthy': preferences.healthy,
            'vegan': preferences.vegan, 'vegetarian': preferences.vegetarian, 'gluten_free': preferences.gluten_free, 'nuts_allergy': preferences.nuts_allergy, 'lactose_intolerant': preferences.lactose_intolerant}
        return(preferences_dict)
    
    def user_login(self, authToken, userEmail, method):
        if not authToken:
            return('Could not authenticate')
        if not userEmail:
            return('Could not authenticate')

        check_user_login = Zatiq_Users.objects(auth_token=authToken)

        if len(check_user_login) > 0:
            user_info = self.get_user_info(authToken, method)
            user_name = user_info['name']
            user_email = user_info['email']
            api_token = check_user_login[0].zatiq_token
            return([user_name, user_email, api_token])
        else:
            return('Could not authenticate')
        
    def user_register(self, authToken, method):
        if not authToken:
            return('Could not authenticate')
        
        check_user_register = Zatiq_Users.objects(auth_token=authToken)
        if len(check_user_register) > 0:
            return(self.user_login(authToken, check_user_register[0].user_email, method))
        else:
            user_info = self.get_user_info(authToken, method)
            user_id = user_info['id']
            user_email = user_info['email']
            user_name = user_info['name']
            api_token = self.generate_zatiq_api_token()

            if method == 'google':
                if self.check_user_exists(user_email, user_id, method, authToken) == False:
                    user_register = Zatiq_Users.objects(auth_token=authToken).update_one(upsert=True, set__user_email=user_email, set__user_name=user_name, set__google_id=user_id, set__zatiq_token=api_token,
                        set__preferences__halal=False, set__preferences__spicy=True, set__preferences__kosher=False, set__preferences__healthy=False, set__preferences__vegan=False, set__preferences__vegetarian=False,
                        set__preferences__gluten_free=False, set__preferences__nuts_allergy=True, set__preferences__lactose_intolerant=False)
                    return(self.user_login(authToken, user_email, method))
                else:
                    return(self.user_login(authToken, user_email, method))

            if method == 'facebook':
                if self.check_user_exists(user_email, user_id, method, authToken) == False:
                    user_register = Zatiq_Users.objects(auth_token=authToken).update_one(upsert=True, set__user_email=user_email, set__user_name=user_name, set__facebook_id=user_id, set__zatiq_token=api_token,
                    set__preferences__halal=False, set__preferences__spicy=True, set__preferences__kosher=False, set__preferences__healthy=False, set__preferences__vegan=False, set__preferences__vegetarian=False,
                    set__preferences__gluten_free=False, set__preferences__nuts_allergy=True, set__preferences__lactose_intolerant=False)
                    return(self.user_login(authToken, user_email, method))
                else:
                    return(self.user_login(authToken, user_email, method))

    def update_user_preferences(self, api_token, preferences):
        if not api_token:
            return('Could not authenticate')
        
        if self.check_valid_api_token(api_token) == True:
            user_id = self.get_user_id_by_api_token(api_token)
            if user_id != None:
                try:
                    Zatiq_Users.objects(zatiq_token=api_token).update_one(upsert=False,
                        set__preferences__halal=preferences['halal'], set__preferences__spicy=preferences['spicy'], set__preferences__kosher=preferences['kosher'], set__preferences__healthy=preferences['healthy'],
                        set__preferences__vegan=preferences['vegan'], set__preferences__vegetarian=preferences['vegetarian'], set__preferences__gluten_free=preferences['gluten_free'], set__preferences__nuts_allergy=preferences['nuts_allergy'],
                        set__preferences__lactose_intolerant=preferences['lactose_intolerant'])
                except Exception as e:
                    return("Error \n %s" % (e))
                try:
                    get_user_info = Zatiq_Users.objects(zatiq_token=api_token)
                except Exception as e:
                    return("Error \n %s" % (e))
                user_email = get_user_info[0].user_email
                auth_token = get_user_info[0].auth_token
                user_name = get_user_info[0].user_name
                preferences = self.generate_preferences_dict(get_user_info[0].preferences)
                return([user_email, auth_token, user_name, preferences])
            else:
                return('No such user')
        else:
            return('Could not authenticate')

        def get_food_items_by_cuisine_type(self, api_token, cuisine_type):
            if not api_token:
                return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                food_items = Zatiq_Food_Items.objects.filter('tags__{}=True'.join(cuisine_type))
            except Exception as e:
                return("Error \n %s" % (e))
            
            if len(food_items) > 0:
                food_items_dict = self.generate_food_items_dict(food_items)
                return(food_items_dict)
            else:
                return([])
        else:
            return('Could not authenticate')

    def get_food_items_by_time_of_day(self, api_token, time):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                food_items = Zatiq_Food_Items.objects.filter('meal_type__{}=True'.join(time))
            except Exception as e:
                return("Error \n %s" % (e))

            if len(food_items) > 0:
                food_items_dict = self.generate_food_items_dict(food_items)
                return(food_items_dict)
            else:
                return([])
        else:
            return('Could not authenticate')

    def generate_food_items_dict(self, food_items):
        food_items_list = []
        for food_item in range(len(food_items)):
            food_item_id = food_items[food_item].id
            restaurant_id = food_items[food_item].restaurant_id
            item_name = food_items[food_item].item_name
            overview = food_items[food_item].overview
            image = food_items[food_item].image
            item_price = food_items[food_item].item_price
            is_beverage = food_items[food_item].is_beverage
            meal_types = self.generate_meals_dict(food_items[food_item].meal_type)
            image_aspect_ratio = food_items[food_item].image_aspect_ratio
            tags = self.generate_tags_dict(food_items[food_item].tags, is_beverage)
            meats = self.generate_meats_dict(food_items[food_item].tags.meat)
            seafoods = self.generate_seafoods_dict(food_items[food_item].tags.seafood)
            food_item_info = {'food_item_id': str(food_item_id), 'restaurant_id': str(restaurant_id), 'item_name': item_name, 'meal_type': meal_types, 'item_price': item_price, 'overview': overview, 'image': {'base64': image, 'image_aspect_ratio': image_aspect_ratio}, 'tags': tags, 'meat': meats, 'seafood': seafoods}
            food_items_list.append(food_item_info)
        return(food_items_list)

    def generate_tags_dict(self, tags, is_beverage):
        tags_dict = {'indian': tags.indian, 'greek': tags.greek, 'chinese': tags.chinese, 'japanese': tags.japanese, 'korean': tags.korean, 'sushi': tags.sushi, 'dessert': tags.dessert, 'burger': tags.burger,
            'pizza': tags.pizza, 'fast_food': tags.fast_food, 'halal': tags.halal, 'caribbean': tags.caribbean, 'mexican': tags.mexican, 'spicy': tags.spicy, 'fine_food': tags.fine_food, 'kosher': tags.kosher,
            'healthy': tags.healthy, 'vegan': tags.vegan, 'vegetarian': tags.vegetarian, 'gluten_free': tags.gluten_free, 'italian': tags.italian, 'middle_eastern': tags.middle_eastern, 'snack': tags.snack, 'thai': tags.thai,
            'canadian': tags.canadian, 'vietnamese': tags.vietnamese, 'has_nuts': tags.has_nuts, 'lactose_free': tags.lactose_free, 'is_beverage': is_beverage}
        return(tags_dict)

    def generate_meals_dict(self, meal_types):
        meals_dict = {'breakfast': meal_types.breakfast, 'lunch': meal_types.lunch, 'dinner': meal_types.dinner, 'brunch': meal_types.brunch}
        return(meals_dict)

    def generate_meats_dict(self, meats):
        meats_dict = {'bear': meats.bear, 'beef': meats.beef, 'buffalo': meats.buffalo, 'calf': meats.calf, 'caribou': meats.caribou, 'goat': meats.goat, 'ham': meats.ham, 'horse': meats.horse, 'kangaroo': meats.kangaroo, 'lamb': meats.lamb,
            'moose': meats.moose, 'mutton': meats.mutton, 'opossum': meats.opossum, 'pork': meats.pork, 'bacon': meats.bacon, 'rabbit': meats.rabbit, 'snake': meats.snake, 'squirrel': meats.squirrel, 'turtle': meats.turtle, 'veal': meats.veal,
            'chicken': meats.chicken, 'hen': meats.hen, 'duck': meats.duck, 'goose': meats.goose, 'ostrich': meats.ostrich, 'quail': meats.quail, 'turkey': meats.turkey}
        return(meats_dict)

    def generate_seafoods_dict(self, sea):
        seafoods_dict = {'clam': sea.clam, 'pangasius': sea.pangasius, 'cod': sea.cod, 'crab': sea.crab, 'catfish': sea.catfish, 'alaska_pollack': sea.alaska_pollack, 'tilapia': sea.tilapia, 'salmon': sea.salmon, 'tuna': sea.tuna, 'shrimp': sea.shrimp,
            'lobster': sea.lobster, 'eel': sea.eel, 'trout': sea.trout, 'pike': sea.pike, 'shark': sea.shark}
        return(seafoods_dict)

