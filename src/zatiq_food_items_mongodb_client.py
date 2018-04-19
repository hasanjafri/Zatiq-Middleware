from mongoengine import *
import bson
from zatiq_food_items import Zatiq_Food_Items
from zatiq_businesses import Zatiq_Businesses

class ZatiqFoodItemsMongoDBClient(object):
    def add_food_item(self, image, overview, item_name, api_token, meal_type, tags, item_price, meat, seafood):
        if self.check_valid_api_token(api_token) == True:
            restaurant = self.get_restaurant_id_by_api_token(api_token)
            food_item_id = self.generate_food_item_id()
            try:
                Zatiq_Food_Items.objects(id=food_item_id).update_one(upsert=True, restaurant_id=restaurant, item_name=item_name, image=image['base64'], image_aspect_ratio=image['image_aspect_ratio'], overview=overview, is_beverage=tags['is_beverage'], item_price=item_price,
                set__tags__indian=tags['indian'], set__tags__greek=tags['greek'], set__tags__chinese=tags['chinese'], set__tags__japanese=tags['japanese'], set__tags__korean=tags['korean'], set__tags__sushi=tags['sushi'], set__tags__dessert=tags['dessert'], set__tags__burger=tags['burger'], set__tags__pizza=tags['pizza'],
                set__tags__fast_food=tags['fast_food'], set__tags__halal=tags['halal'], set__tags__caribbean=tags['caribbean'], set__tags__mexican=tags['mexican'], set__tags__spicy=tags['spicy'], set__tags__fine_food=tags['fine_food'], set__tags__kosher=tags['kosher'], set__tags__healthy=tags['healthy'], set__tags__vegan=tags['vegan'], set__tags__vegetarian=tags['vegetarian'],
                set__tags__gluten_free=tags['gluten_free'], set__tags__italian=tags['italian'], set__tags__middle_eastern=tags['middle_eastern'], set__tags__snack=tags['snack'], set__tags__thai=tags['thai'], set__tags__canadian=tags['canadian'], set__tags__vietnamese=tags['vietnamese'], set__tags__has_nuts=tags['has_nuts'], set__tags__lactose_free=tags['lactose_free'],
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
    
    def update_food_item(self, api_token, food_item_id, image, overview, item_name, meal_type, tags, item_price, meat, seafood):
        if self.check_valid_api_token(api_token) == True:
            restaurant_id = self.get_restaurant_id_by_api_token(api_token)
            try:
                Zatiq_Food_Items.objects(id=food_item_id, restaurant_id=restaurant_id).update_one(upsert=False, item_name=item_name, image=image['base64'], image_aspect_ratio=image['image_aspect_ratio'], overview=overview, is_beverage=tags['is_beverage'], item_price=item_price,
                set__tags__indian=tags['indian'], set__tags__greek=tags['greek'], set__tags__chinese=tags['chinese'], set__tags__japanese=tags['japanese'], set__tags__korean=tags['korean'], set__tags__sushi=tags['sushi'], set__tags__dessert=tags['dessert'], set__tags__burger=tags['burger'], set__tags__pizza=tags['pizza'],
                set__tags__fast_food=tags['fast_food'], set__tags__halal=tags['halal'], set__tags__caribbean=tags['caribbean'], set__tags__mexican=tags['mexican'], set__tags__spicy=tags['spicy'], set__tags__fine_food=tags['fine_food'], set__tags__kosher=tags['kosher'], set__tags__healthy=tags['healthy'], set__tags__vegan=tags['vegan'], set__tags__vegetarian=tags['vegetarian'],
                set__tags__gluten_free=tags['gluten_free'], set__tags__italian=tags['italian'], set__tags__middle_eastern=tags['middle_eastern'], set__tags__snack=tags['snack'], set__tags__thai=tags['thai'], set__tags__canadian=tags['canadian'], set__tags__vietnamese=tags['vietnamese'], set__tags__has_nuts=tags['has_nuts'], set__tags__lactose_free=tags['lactose_free'],
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
            try:
                Zatiq_Food_Items.objects(id=food_item_id, restaurant_id=restaurant_id).delete()
            except Exception as e:
                return("Error \n %s" %(e))
            return('Food item deleted')
        else:
            return('Could not authenticate')

    def generate_food_item_id(self):
        food_item_id = bson.objectid.ObjectId()
        return(food_item_id)

    def get_food_by_tags(self, tags):
        pass

    def get_restaurant_id_by_api_token(self, api_token):
        valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if (len(valid_token) > 0):
            restaurant_id = valid_token[0].id
            return(restaurant_id)
        else:
            return(None)

    def get_food_items_by_restaurant_id(self, api_token):
        if self.check_valid_api_token(api_token) == True:
            restaurant_id = self.get_restaurant_id_by_api_token(api_token)
            try:
                foods_by_restaurant = Zatiq_Food_Items.objects(restaurant_id=restaurant_id)
            except Exception as e:
                return("Error \n %s" % (e))
            if len(foods_by_restaurant) > 0:
                food_items_dict = self.generate_food_items_dict(foods_by_restaurant)
                return(food_items_dict)
            else:
                return([])
                
    def check_valid_api_token(self, api_token):
        valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if len(valid_token) > 0:
            return(True)
        else:
            return(False)

    def get_food_by_id(self, api_token, food_item_id):
        if self.check_valid_api_token(api_token) == True:
            try:
                food_item = Zatiq_Food_Items.objects(id=food_item_id)
            except Exception as e:
                return("Error \n %s" %(e))
            if len(food_item) > 0:
                food_item_dict = self.generate_food_items_dict(food_item)
                return(food_item_dict)
            else:
                return('No food item found with that id')
                

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

    def get_food_items_by_cuisine_type(self, api_token, cuisine_type):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            try:
                food_items = Zatiq_Food_Items.objects(tags[cuisine_type]=True)
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
                food_items = Zatiq_Food_Items.objects(meal_type[time]=True)
            except Exception as e:
                return("Error \n %s" % (e))

            if len(food_items) > 0:
                food_items_dict = self.generate_food_items_dict(food_items)
                return(food_items_dict)
            else:
                return([])
        else:
            return('Could not authenticate')
                    
