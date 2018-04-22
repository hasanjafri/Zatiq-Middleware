from mongoengine import *
import secrets
import requests
import json
from zatiq_users import Zatiq_Users
from zatiq_food_items import Zatiq_Food_Items
from zatiq_menus import Zatiq_Menus
from zatiq_interiors import Zatiq_Interiors

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

    def get_menu_pictures(self, api_token, restaurant_id):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                menu_pictures = Zatiq_Menus.objects(restaurant_id=restaurant_id)
            except Exception as e:
                return("Error \n %s" % (e))

            result = self.generate_photos_dict(menu_pictures)
            return(result)
        else:
            return('Could not authenticate')

    def get_interior_pictures(self, api_token, restaurant_id):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                interior_pictures = Zatiq_Interiors.objects(restaurant_id=restaurant_id)
            except Exception as e:
                return("Error \n %s" % (e))

            result = self.generate_photos_dict(interior_pictures)
            return(result)
        else:
            return('Could not authenticate')

    def generate_photos_dict(self, photos):
        photos_list = []
        for photo in range(len(photos)):
            image_id = str(photos[photo].id)
            base64 = photos[photo].image
            image_aspect_ratio = photos[photo].image_aspect_ratio
            photo_info = {'image_id': image_id, 'image': {
                'base64': base64, 'image_aspect_ratio': image_aspect_ratio}}
            photos_list.append(photo_info)
        return(photos_list)
