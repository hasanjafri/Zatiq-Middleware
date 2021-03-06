from mongoengine import *
import bson
import random
from zatiq_food_items import Zatiq_Food_Items
from zatiq_businesses import Zatiq_Businesses
from zatiq_users import Zatiq_Users
from requests import post

class ZatiqFoodItemsMongoDBClient(object):
    def add_food_item(self, image, overview, item_name, api_token, meal_type, tags, item_price, meat, seafood, calories):
        if self.check_valid_api_token(api_token) == True:
            image_url = post("http://167.99.177.29:5000/upload/", json={'imagedata': image['base64']})
            if 'Error' in image_url:
                return("Invalid image provided")
            restaurant = self.get_restaurant_id_by_api_token(api_token)
            food_item_id = self.generate_food_item_id()
            try:
                Zatiq_Food_Items.objects(id=food_item_id).update_one(upsert=True, restaurant_id=restaurant, item_name=item_name, image=image_url.text, image_aspect_ratio=image['image_aspect_ratio'], overview=overview, is_beverage=tags['is_beverage'], item_price=item_price, calories=calories,
                set__tags__indian=tags['indian'], set__tags__greek=tags['greek'], set__tags__chinese=tags['chinese'], set__tags__japanese=tags['japanese'], set__tags__korean=tags['korean'], set__tags__sushi=tags['sushi'], set__tags__dessert=tags['dessert'], set__tags__burger=tags['burger'], set__tags__pizza=tags['pizza'],
                set__tags__fast_food=tags['fast_food'], set__tags__halal=tags['halal'], set__tags__caribbean=tags['caribbean'], set__tags__mexican=tags['mexican'], set__tags__spicy=tags['spicy'], set__tags__fine_food=tags['fine_food'], set__tags__kosher=tags['kosher'], set__tags__healthy=tags['healthy'], set__tags__vegan=tags['vegan'], set__tags__vegetarian=tags['vegetarian'],
                set__tags__gluten_free=tags['gluten_free'], set__tags__italian=tags['italian'], set__tags__middle_eastern=tags['middle_eastern'], set__tags__snack=tags['snack'], set__tags__thai=tags['thai'], set__tags__canadian=tags['canadian'], set__tags__vietnamese=tags['vietnamese'], set__tags__has_soybeans=tags['has_soybeans'], set__tags__has_eggs=tags['has_eggs'], set__tags__jain=tags['jain'], set__tags__has_wheat=tags['has_wheat'], set__tags__has_treenuts=tags['has_treenuts'], set__tags__has_peanuts=tags['has_peanuts'], set__tags__lactose_free=tags['lactose_free'],
                set__tags__meat__bear=meat['bear'], set__tags__meat__beef=meat['beef'], set__tags__meat__buffalo=meat['buffalo'], set__tags__meat__calf=meat['calf'], set__tags__meat__caribou=meat['caribou'], set__tags__meat__goat=meat['goat'], set__tags__meat__ham=meat['ham'], set__tags__meat__horse=meat['horse'], set__tags__meat__kangaroo=meat['kangaroo'], set__tags__meat__lamb=meat['lamb'], set__tags__meat__moose=meat['moose'], set__tags__meat__mutton=meat['mutton'], set__tags__meat__opossum=meat['opossum'],
                set__tags__meat__pork=meat['pork'], set__tags__meat__bacon=meat['bacon'], set__tags__meat__rabbit=meat['rabbit'], set__tags__meat__snake=meat['snake'], set__tags__meat__squirrel=meat['squirrel'], set__tags__meat__turtle=meat['turtle'], set__tags__meat__veal=meat['veal'], set__tags__meat__chicken=meat['chicken'], set__tags__meat__hen=meat['hen'], set__tags__meat__duck=meat['duck'], set__tags__meat__goose=meat['goose'],
                set__tags__meat__ostrich=meat['ostrich'], set__tags__meat__quail=meat['quail'], set__tags__meat__turkey=meat['turkey'], set__tags__seafood__clam=seafood['clam'], set__tags__seafood__pangasius=seafood['pangasius'], set__tags__seafood__cod=seafood['cod'], set__tags__seafood__crab=seafood['crab'], set__tags__seafood__catfish=seafood['catfish'], set__tags__seafood__alaska_pollack=seafood['alaska_pollack'], set__tags__seafood__tilapia=seafood['tilapia'], set__tags__seafood__salmon=seafood['salmon'], set__tags__seafood__tuna=seafood['tuna'],
                set__tags__seafood__shrimp=seafood['shrimp'], set__tags__seafood__lobster=seafood['lobster'], set__tags__seafood__eel=seafood['eel'], set__tags__seafood__trout=seafood['trout'], set__tags__seafood__pike=seafood['pike'], set__tags__seafood__shark=seafood['shark'], set__meal_type__breakfast=meal_type['breakfast'], set__meal_type__lunch=meal_type['lunch'], set__meal_type__dinner=meal_type['dinner'])
            except Exception as e:
                return("Error \n %s" % (e))
            new_food_item_id = Zatiq_Food_Items.objects(id=food_item_id)[0].id
            return({'food_item_id': str(new_food_item_id)})
        else:
            return('Could not authenticate')
    
    def update_food_item_without_image(self, api_token, food_item_id, overview, item_name, meal_type, tags, item_price, meat, seafood, calories):
        if self.check_valid_api_token(api_token) == True:
            restaurant_id = self.get_restaurant_id_by_api_token(api_token)
            try:
                Zatiq_Food_Items.objects(id=food_item_id, restaurant_id=restaurant_id).update_one(upsert=False, item_name=item_name, overview=overview, is_beverage=tags['is_beverage'], item_price=item_price, calories=calories,
                set__tags__indian=tags['indian'], set__tags__greek=tags['greek'], set__tags__chinese=tags['chinese'], set__tags__japanese=tags['japanese'], set__tags__korean=tags['korean'], set__tags__sushi=tags['sushi'], set__tags__dessert=tags['dessert'], set__tags__burger=tags['burger'], set__tags__pizza=tags['pizza'],
                set__tags__fast_food=tags['fast_food'], set__tags__halal=tags['halal'], set__tags__caribbean=tags['caribbean'], set__tags__mexican=tags['mexican'], set__tags__spicy=tags['spicy'], set__tags__fine_food=tags['fine_food'], set__tags__kosher=tags['kosher'], set__tags__healthy=tags['healthy'], set__tags__vegan=tags['vegan'], set__tags__vegetarian=tags['vegetarian'],
                set__tags__gluten_free=tags['gluten_free'], set__tags__italian=tags['italian'], set__tags__middle_eastern=tags['middle_eastern'], set__tags__snack=tags['snack'], set__tags__thai=tags['thai'], set__tags__canadian=tags['canadian'], set__tags__vietnamese=tags['vietnamese'], set__tags__has_soybeans=tags['has_soybeans'], set__tags__has_eggs=tags['has_eggs'], set__tags__jain=tags['jain'], set__tags__has_wheat=tags['has_wheat'], set__tags__has_treenuts=tags['has_treenuts'], set__tags__has_peanuts=tags['has_peanuts'], set__tags__lactose_free=tags['lactose_free'],
                set__tags__meat__bear=meat['bear'], set__tags__meat__beef=meat['beef'], set__tags__meat__buffalo=meat['buffalo'], set__tags__meat__calf=meat['calf'], set__tags__meat__caribou=meat['caribou'], set__tags__meat__goat=meat['goat'], set__tags__meat__ham=meat['ham'], set__tags__meat__horse=meat['horse'], set__tags__meat__kangaroo=meat['kangaroo'], set__tags__meat__lamb=meat['lamb'], set__tags__meat__moose=meat['moose'], set__tags__meat__mutton=meat['mutton'], set__tags__meat__opossum=meat['opossum'],
                set__tags__meat__pork=meat['pork'], set__tags__meat__bacon=meat['bacon'], set__tags__meat__rabbit=meat['rabbit'], set__tags__meat__snake=meat['snake'], set__tags__meat__squirrel=meat['squirrel'], set__tags__meat__turtle=meat['turtle'], set__tags__meat__veal=meat['veal'], set__tags__meat__chicken=meat['chicken'], set__tags__meat__hen=meat['hen'], set__tags__meat__duck=meat['duck'], set__tags__meat__goose=meat['goose'],
                set__tags__meat__ostrich=meat['ostrich'], set__tags__meat__quail=meat['quail'], set__tags__meat__turkey=meat['turkey'], set__tags__seafood__clam=seafood['clam'], set__tags__seafood__pangasius=seafood['pangasius'], set__tags__seafood__cod=seafood['cod'], set__tags__seafood__crab=seafood['crab'], set__tags__seafood__catfish=seafood['catfish'], set__tags__seafood__alaska_pollack=seafood['alaska_pollack'], set__tags__seafood__tilapia=seafood['tilapia'], set__tags__seafood__salmon=seafood['salmon'], set__tags__seafood__tuna=seafood['tuna'],
                set__tags__seafood__shrimp=seafood['shrimp'], set__tags__seafood__lobster=seafood['lobster'], set__tags__seafood__eel=seafood['eel'], set__tags__seafood__trout=seafood['trout'], set__tags__seafood__pike=seafood['pike'], set__tags__seafood__shark=seafood['shark'], set__meal_type__breakfast=meal_type['breakfast'], set__meal_type__lunch=meal_type['lunch'], set__meal_type__dinner=meal_type['dinner'], set__meal_type__brunch=meal_type['brunch'])
            except Exception as e:
                return("Error \n %s" % (e))
            return(['Update successful', food_item_id])
        else:
            return('Could not authenticate')

    def update_food_item_with_image(self, api_token, food_item_id, image, overview, item_name, meal_type, tags, item_price, meat, seafood, calories):
        if self.check_valid_api_token(api_token) == True:
            restaurant_id = self.get_restaurant_id_by_api_token(api_token)
            try:
                old_image_url = Zatiq_Food_Items.objects(id=food_item_id, restaurant_id=restaurant_id)
            except Exception as e:
                return("Error \n %s" % (e))
            image_url = post("http://167.99.177.29:5000/update/", json={'imagedata': image['base64'], 'imagepath': str(old_image_url[0].image)})
            if 'Error' in image_url:
                return("Invalid image provided")
            try:
                Zatiq_Food_Items.objects(id=food_item_id, restaurant_id=restaurant_id).update_one(upsert=False, item_name=item_name, image=image_url.text, image_aspect_ratio=image['image_aspect_ratio'], overview=overview, is_beverage=tags['is_beverage'], item_price=item_price, calories=calories,
                set__tags__indian=tags['indian'], set__tags__greek=tags['greek'], set__tags__chinese=tags['chinese'], set__tags__japanese=tags['japanese'], set__tags__korean=tags['korean'], set__tags__sushi=tags['sushi'], set__tags__dessert=tags['dessert'], set__tags__burger=tags['burger'], set__tags__pizza=tags['pizza'],
                set__tags__fast_food=tags['fast_food'], set__tags__halal=tags['halal'], set__tags__caribbean=tags['caribbean'], set__tags__mexican=tags['mexican'], set__tags__spicy=tags['spicy'], set__tags__fine_food=tags['fine_food'], set__tags__kosher=tags['kosher'], set__tags__healthy=tags['healthy'], set__tags__vegan=tags['vegan'], set__tags__vegetarian=tags['vegetarian'],
                set__tags__gluten_free=tags['gluten_free'], set__tags__italian=tags['italian'], set__tags__middle_eastern=tags['middle_eastern'], set__tags__snack=tags['snack'], set__tags__thai=tags['thai'], set__tags__canadian=tags['canadian'], set__tags__vietnamese=tags['vietnamese'], set__tags__has_soybeans=tags['has_soybeans'], set__tags__has_eggs=tags['has_eggs'], set__tags__jain=tags['jain'], set__tags__has_wheat=tags['has_wheat'], set__tags__has_treenuts=tags['has_treenuts'], set__tags__has_peanuts=tags['has_peanuts'], set__tags__lactose_free=tags['lactose_free'],
                set__tags__meat__bear=meat['bear'], set__tags__meat__beef=meat['beef'], set__tags__meat__buffalo=meat['buffalo'], set__tags__meat__calf=meat['calf'], set__tags__meat__caribou=meat['caribou'], set__tags__meat__goat=meat['goat'], set__tags__meat__ham=meat['ham'], set__tags__meat__horse=meat['horse'], set__tags__meat__kangaroo=meat['kangaroo'], set__tags__meat__lamb=meat['lamb'], set__tags__meat__moose=meat['moose'], set__tags__meat__mutton=meat['mutton'], set__tags__meat__opossum=meat['opossum'],
                set__tags__meat__pork=meat['pork'], set__tags__meat__bacon=meat['bacon'], set__tags__meat__rabbit=meat['rabbit'], set__tags__meat__snake=meat['snake'], set__tags__meat__squirrel=meat['squirrel'], set__tags__meat__turtle=meat['turtle'], set__tags__meat__veal=meat['veal'], set__tags__meat__chicken=meat['chicken'], set__tags__meat__hen=meat['hen'], set__tags__meat__duck=meat['duck'], set__tags__meat__goose=meat['goose'],
                set__tags__meat__ostrich=meat['ostrich'], set__tags__meat__quail=meat['quail'], set__tags__meat__turkey=meat['turkey'], set__tags__seafood__clam=seafood['clam'], set__tags__seafood__pangasius=seafood['pangasius'], set__tags__seafood__cod=seafood['cod'], set__tags__seafood__crab=seafood['crab'], set__tags__seafood__catfish=seafood['catfish'], set__tags__seafood__alaska_pollack=seafood['alaska_pollack'], set__tags__seafood__tilapia=seafood['tilapia'], set__tags__seafood__salmon=seafood['salmon'], set__tags__seafood__tuna=seafood['tuna'],
                set__tags__seafood__shrimp=seafood['shrimp'], set__tags__seafood__lobster=seafood['lobster'], set__tags__seafood__eel=seafood['eel'], set__tags__seafood__trout=seafood['trout'], set__tags__seafood__pike=seafood['pike'], set__tags__seafood__shark=seafood['shark'], set__meal_type__breakfast=meal_type['breakfast'], set__meal_type__lunch=meal_type['lunch'], set__meal_type__dinner=meal_type['dinner'], set__meal_type__brunch=meal_type['brunch'])
            except Exception as e:
                return("Error \n %s" % (e))
            return(['Update successful', food_item_id])
        else:
            return('Could not authenticate')

    def delete_food_item(self, api_token, food_item_id):
        if self.check_valid_api_token(api_token) == True:
            restaurant_id = self.get_restaurant_id_by_api_token(api_token)
            local_image_path = Zatiq_Food_Items.objects(id=food_item_id, restaurant_id=restaurant_id)[0].image
            try:
                Zatiq_Food_Items.objects(id=food_item_id, restaurant_id=restaurant_id).delete()
            except Exception as e:
                return("Error \n %s" %(e))
                
            delete_image = post("http://167.99.177.29:5000/delete/", json={'imagepath': local_image_path})
            if 'Error' in delete_image:
                with open('./food_delete_failed.txt', 'a') as file:
                    file.write('(food_id:{}, restaurant_id:{})\n'.format(food_item_id, restaurant_id))
            return('Food item deleted')
        else:
            return('Could not authenticate')

    def generate_food_item_id(self):
        food_item_id = bson.objectid.ObjectId()
        return(food_item_id)

    def get_restaurant_id_by_api_token(self, api_token):
        valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if (len(valid_token) > 0):
            restaurant_id = valid_token[0].id
            return(restaurant_id)
        else:
            return(None)

    def get_food_items_by_restaurant_id(self, api_token, restaurant_id):
        if restaurant_id == None:
            restaurant_id = self.get_restaurant_id_by_api_token(api_token)
        try:
            foods_by_restaurant = Zatiq_Food_Items.objects(restaurant_id=restaurant_id)
        except Exception as e:
            return("Error \n %s" % (e))
        if len(foods_by_restaurant) > 0:
            food_items_dict = self.generate_food_items_dict_full(foods_by_restaurant)
            return(food_items_dict)
        else:
            return([])

    def find_food_grid(self, api_token):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                zatiq_food_items = Zatiq_Food_Items.objects()
            except Exception as e:
                return("Error \n %s" % (e))

            if len(zatiq_food_items) > 0:
                if self.check_user(api_token) == 'user':
                    user_preferences = self.get_user_preferences(api_token)
                    filtered_food = self.filter_food(zatiq_food_items, user_preferences)

                    if len(filtered_food) > 25:
                        food_items_dict = self.generate_food_items_dict_full(filtered_food[0:25])
                        return(food_items_dict)
                    else:
                        food_items_dict = self.generate_food_items_dict_full(filtered_food)
                        return(food_items_dict)
                else:
                    food_items_dict = self.generate_food_items_dict_full(zatiq_food_items)
                    return(food_items_dict)
            else:
                return([])
        else:
            return('Could not authenticate')

    def filter_food(self, food_items, preferences):
        filtered_items = []
        for food_item in food_items:
           if self.check_food_item(food_item, preferences) == True:
               filtered_items.append(food_item)
        return(filtered_items)

    def check_food_item(self, food_item, preferences):
        for preference in preferences:
            if preference == 'omnivore':
                continue
            elif preference == 'milk_allergy':
                continue
            elif preference == 'fish_allergy':
                for seafood_type in food_item.tags.seafood:
                    if food_item.tags.seafood[seafood_type] == True:
                        return(False)
            elif preference == 'crustacean_allergy':
                crustaceans = ['crab', 'lobster', 'shrimp']
                for crustacean_type in crustaceans:
                    if food_item.tags.seafood[crustacean_type] == True:
                        return(False)
            elif preference == 'pescatarian':
                for meat_type in food_item.tags.meat:
                    if food_item.tags.meat[meat_type] == True:
                        return(False)
            elif preference == 'has_eggs':
                if food_item.tags['has_eggs'] == True:
                    return(False)
            elif preference == 'has_peanuts':
                if food_item.tags['has_peanuts'] == True:
                    return(False)
            elif preference == 'has_treenuts':
                if food_item.tags['has_treenuts'] == True:
                    return(False)
            elif preference == 'has_soybeans':
                if food_item.tags['has_soybeans'] == True:
                    return(False)
            elif preference == 'has_wheat':
                if food_item.tags['has_wheat'] == True:
                    return(False)
            else:
                if food_item.tags[preference] == False:
                    return(False)
        return(True)

    def find_food_grid_by_name(self, api_token, name):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                zatiq_food_items = Zatiq_Food_Items.objects.search_text(name)
            except Exception as e:
                return("Error \n %s" % (e))

            if len(zatiq_food_items) > 0:
                if len(zatiq_food_items) > 25:
                    food_items_dict = self.generate_food_items_dict_full(zatiq_food_items[0:25])
                    return(food_items_dict)
                else:
                    food_items_dict = self.generate_food_items_dict_full(zatiq_food_items)
                    return(food_items_dict)
            else:
                return([])
        else:
            return('Could not authenticate')
                
    def check_valid_api_token(self, api_token):
        try:
            valid_token = Zatiq_Users.objects(zatiq_token=api_token)
        except Exception as e:
            return("Error \n %s" % (e))
        if len(valid_token) > 0:
            return(True)
        else:
            try:
                valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
            except Exception as e:
                return("Error \n %s" % (e))
            if len(valid_token) > 0:
                return(True)
            else:
                return(False)

    def get_food_by_id(self, food_item_id):
        try:
            food_item = Zatiq_Food_Items.objects(id=food_item_id)
        except Exception as e:
            return("Error \n %s" %(e))
        if len(food_item) > 0:
            food_item_dict = self.generate_food_items_dict(food_item)
            return(food_item_dict)
        else:
            return('No food item found with that id')

    def get_restaurant_info(self, restaurant_id):
        try:
            zatiq_business = Zatiq_Businesses.objects(id=restaurant_id)
        except Exception as e:
            return("Error \n %s" % (e))

        if len(zatiq_business) > 0:
            restaurant_id = zatiq_business[0].id
            email = zatiq_business[0].business_email
            name = zatiq_business[0].business_name
            website = zatiq_business[0].website
            hours = self.generate_business_hours(zatiq_business[0].hours)
            number = zatiq_business[0].number
            features = {'delivery': zatiq_business[0].delivery, 'takeout': zatiq_business[0].takeout, 'reservation': zatiq_business[0].reservation, 'patio': zatiq_business[0].patio, 'wheelchair_accessible': zatiq_business[0].wheelchair_accessible, 'parking': zatiq_business[0].parking, 'buffet': zatiq_business[0].buffet, 'family_friendly': zatiq_business[0].family_friendly, 'pescetarian_friendly': zatiq_business[0].pescetarian_friendly, 'wifi': zatiq_business[0].wifi}
            image = {'base64': "http://167.99.177.29:5000/image/"+str(zatiq_business[0].image), 'image_aspect_ratio': zatiq_business[0].image_aspect_ratio}
            
            address = zatiq_business[0].address
            restaurant_info = {'restaurant_id': str(restaurant_id), 'email': email, 'name': name, 'website': website, 'hours': hours, 'number': number, 'features': features, 'image': image, 'address': address}
            return(restaurant_info)
        else:
            return('Could not find a restaurant with that id')

    def generate_business_hours(self, business):
        hours_dict = {'start': {
            'monday': business.monday_start,
            'tuesday': business.tuesday_start,
            'wednesday': business.wednesday_start,
            'thursday': business.thursday_start,
            'friday': business.friday_start,
            'saturday': business.saturday_start,
            'sunday': business.sunday_start
        }, 'end': {
            'monday': business.monday_end,
            'tuesday': business.tuesday_end,
            'wednesday': business.wednesday_end,
            'thursday': business.thursday_end,
            'friday': business.friday_end,
            'saturday': business.saturday_end,
            'sunday': business.sunday_end
        }}
        return(hours_dict)

    def generate_food_items_dict(self, food_items):
        food_items_list = []
        for food_item in range(len(food_items)):
            try:
                Zatiq_Food_Items.objects(id=food_items[food_item].id).modify(inc__views=1)
            except Exception as e:
                print("Error \n %s" % (e))
            food_item_id = food_items[food_item].id
            restaurant_id = food_items[food_item].restaurant_id.id
            restaurant_info = self.get_restaurant_info(restaurant_id)
            item_name = food_items[food_item].item_name
            overview = food_items[food_item].overview
            image = "http://167.99.177.29:5000/image/"+str(food_items[food_item].image)
            item_price = food_items[food_item].item_price
            is_beverage = food_items[food_item].is_beverage
            meal_types = self.generate_meals_dict(food_items[food_item].meal_type)
            image_aspect_ratio = food_items[food_item].image_aspect_ratio
            tags = self.generate_tags_dict(food_items[food_item].tags, is_beverage)
            meats = self.generate_meats_dict(food_items[food_item].tags.meat)
            seafoods = self.generate_seafoods_dict(food_items[food_item].tags.seafood)
            calories = food_items[food_item].calories
            food_item_info = {'food_item_id': str(food_item_id), 'restaurant_id': str(restaurant_id), 'restaurant_info': restaurant_info, 'item_name': item_name, 'meal_type': meal_types, 'item_price': str(item_price), 'overview': overview, 'image': {'base64': image, 'image_aspect_ratio': image_aspect_ratio}, 'tags': tags, 'meat': meats, 'seafood': seafoods, 'calories': calories}
            food_items_list.append(food_item_info)
            if len(food_items_list) > 5:
                food_items_list = random.sample(food_items_list, 5)
        return(food_items_list)

    def generate_food_items_dict_full(self, food_items):
        food_items_list = []
        for food_item in range(len(food_items)):
            try:
                Zatiq_Food_Items.objects(id=food_items[food_item].id).modify(inc__views=1)
            except Exception as e:
                print("Error \n %s" % (e))
            food_item_id = food_items[food_item].id
            restaurant_id = food_items[food_item].restaurant_id.id
            restaurant_info = self.get_restaurant_info(restaurant_id)
            item_name = food_items[food_item].item_name
            overview = food_items[food_item].overview
            image = "http://167.99.177.29:5000/image/"+str(food_items[food_item].image)
            item_price = food_items[food_item].item_price
            is_beverage = food_items[food_item].is_beverage
            meal_types = self.generate_meals_dict(food_items[food_item].meal_type)
            image_aspect_ratio = food_items[food_item].image_aspect_ratio
            tags = self.generate_tags_dict(food_items[food_item].tags, is_beverage)
            meats = self.generate_meats_dict(food_items[food_item].tags.meat)
            seafoods = self.generate_seafoods_dict(food_items[food_item].tags.seafood)
            calories = food_items[food_item].calories
            food_item_info = {'food_item_id': str(food_item_id), 'restaurant_id': str(restaurant_id), 'restaurant_info': restaurant_info, 'item_name': item_name, 'meal_type': meal_types, 'item_price': str(item_price), 'overview': overview, 'image': {'base64': image, 'image_aspect_ratio': image_aspect_ratio}, 'tags': tags, 'meat': meats, 'seafood': seafoods, 'calories': calories}
            food_items_list.append(food_item_info)
        return(food_items_list)

    def generate_tags_dict(self, tags, is_beverage):
        tags_dict = {'indian': tags.indian, 'greek': tags.greek, 'chinese': tags.chinese, 'japanese': tags.japanese, 'korean': tags.korean, 'sushi': tags.sushi, 'dessert': tags.dessert, 'burger': tags.burger,
            'pizza': tags.pizza, 'fast_food': tags.fast_food, 'halal': tags.halal, 'caribbean': tags.caribbean, 'mexican': tags.mexican, 'spicy': tags.spicy, 'fine_food': tags.fine_food, 'kosher': tags.kosher,
            'healthy': tags.healthy, 'vegan': tags.vegan, 'vegetarian': tags.vegetarian, 'gluten_free': tags.gluten_free, 'italian': tags.italian, 'middle_eastern': tags.middle_eastern, 'snack': tags.snack, 'thai': tags.thai,
            'canadian': tags.canadian, 'vietnamese': tags.vietnamese, 'has_soybeans': tags.has_soybeans, 'has_eggs': tags.has_eggs, 'jain': tags.jain, 'has_wheat': tags.has_wheat, 'has_treenuts': tags.has_treenuts, 'has_peanuts': tags.has_peanuts, 'lactose_free': tags.lactose_free, 'is_beverage': is_beverage}
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

    def get_user_preferences(self, api_token):
        preferences_list = []

        try:
            zatiq_user = Zatiq_Users.objects(zatiq_token=api_token)
        except Exception as e:
            return("Error \n %s" % (e))

        if len(zatiq_user) > 0:
            for preference in zatiq_user[0].preferences:
                if zatiq_user[0].preferences[preference] == True:
                    preferences_list.append(str(preference))
            print(preferences_list)
            return(preferences_list)
        else:
            return([])

    def check_user(self, api_token):
        try:
            user_token = Zatiq_Users.objects(zatiq_token=api_token)
        except Exception as e:
            return("Error \n %s" % (e))
        if len(user_token) > 0:
            return('user')

    def get_food_items_by_cuisine_type(self, api_token, cuisine_type):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                food_items = Zatiq_Food_Items.objects.filter(**{'tags__{}'.format(cuisine_type): True})
            except Exception as e:
                return("Error \n %s" % (e))
        
            if len(food_items) > 0:
                if self.check_user(api_token) == 'user':
                    user_preferences = self.get_user_preferences(api_token)
                    filtered_food = self.filter_food(food_items, user_preferences)

                    if len(filtered_food) > 0:
                        food_items_dict = self.generate_food_items_dict(filtered_food)
                        return(food_items_dict)
                    else:
                        return([])
                else:
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
                food_items = Zatiq_Food_Items.objects.filter(**{'meal_type__{}'.format(time): True})
            except Exception as e:
                return("Error \n %s" % (e))

            if len(food_items) > 0:
                if self.check_user(api_token) == 'user':
                    user_preferences = self.get_user_preferences(api_token)
                    filtered_food = self.filter_food(food_items, user_preferences)

                    if len(filtered_food) > 0:
                        food_items_dict = self.generate_food_items_dict(filtered_food)
                        return(food_items_dict)
                    else:
                        return([])
                else:
                    food_items_dict = self.generate_food_items_dict(food_items)
                    return(food_items_dict)
            else:
                return([])
        else:
            return('Could not authenticate')

    def get_food_items_by_button(self, api_token, button):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            if button == 'promotions':
                try:
                    food_items = Zatiq_Food_Items.objects.order_by('discount_price')
                except Exception as e:
                    return("Error \n %s" % (e))

                if len(food_items) > 0:
                    if self.check_user(api_token) == 'user':
                        user_preferences = self.get_user_preferences(api_token)
                        filtered_food = self.filter_food(food_items, user_preferences)

                        if len(filtered_food) > 0:
                            food_items_dict = self.generate_food_items_dict(filtered_food)
                            return(food_items_dict)
                        else:
                            return([])
                    else:
                        food_items_dict = self.generate_food_items_dict(food_items)
                        return(food_items_dict)
                else:
                    return([])

            elif button == 'top_picks':
                try:
                    food_items = Zatiq_Food_Items.objects.order_by('-views')
                except Exception as e:
                    return("Error \n %s" % (e))

                if len(food_items) > 0:
                    if self.check_user(api_token) == 'user':
                        user_preferences = self.get_user_preferences(api_token)
                        filtered_food = self.filter_food(food_items, user_preferences)

                        if len(filtered_food) > 0:
                            food_items_dict = self.generate_food_items_dict(filtered_food)
                            return(food_items_dict)
                        else:
                            return([])
                    else:
                        food_items_dict = self.generate_food_items_dict(food_items)
                        return(food_items_dict)
                else:
                    return([])

            elif button == 'newest':
                try:
                    food_items = Zatiq_Food_Items.objects.order_by('-date_created')
                except Exception as e:
                    return("Error \n %s" % (e)) 

                if len(food_items) > 0:
                    if self.check_user(api_token) == 'user':
                        user_preferences = self.get_user_preferences(api_token)
                        filtered_food = self.filter_food(food_items, user_preferences)

                        if len(filtered_food) > 0:
                            food_items_dict = self.generate_food_items_dict(filtered_food)
                            return(food_items_dict)
                        else:
                            return([])
                    else:
                        food_items_dict = self.generate_food_items_dict(food_items)
                        return(food_items_dict)
                else:
                    return([])

            elif button == 'surprise_me':
                try:
                    food_items = Zatiq_Food_Items.objects.order_by('views')
                except Exception as e:
                    return("Error \n %s" % (e))

                if len(food_items) > 0:
                    if self.check_user(api_token) == 'user':
                        user_preferences = self.get_user_preferences(api_token)
                        filtered_food = self.filter_food(food_items, user_preferences)

                        if len(filtered_food) > 0:
                            food_items_dict = self.generate_food_items_dict(filtered_food)
                            return(food_items_dict)
                        else:
                            return([])
                    else:
                        food_items_dict = self.generate_food_items_dict(food_items)
                        return(food_items_dict)
                else:
                    return([])
            else:
                return('Category not found')
        else:
            return('Could not authenticate')                    
