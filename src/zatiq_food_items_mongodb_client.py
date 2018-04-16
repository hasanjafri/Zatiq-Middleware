from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_businesses import Zatiq_Businesses

class ZatiqFoodItemsMongoDBClient(object):
    def add_food_item(self, image, overview, item_name, api_token, meal_type, tags, item_price, meat, seafood):
        if self.check_valid_api_token(api_token) == True:
            restaurant = self.get_restaurant_id_by_api_token(api_token)
            try:
                add_food_item = Zatiq_Food_Items(restaurant_id=restaurant, item_name=item_name, image=image['base64'], image_aspect_ratio=image['image_aspect_ratio'], overview=overview, is_beverage=tags['is_beverage'], item_price=item_price,
                tags__indian=tags['indian'], tags__greek=tags['greek'], tags__chinese=tags['chinese'], tags__japanese=tags['japanese'], tags__korean=tags['korean'], tags__sushi=tags['sushi'], tags_dessert=tags['dessert'], tags__burger=tags['burger'], tags__pizza=tags['pizza'],
                tags__fast__food=tags['fast_food'], tags__halal=tags['halal'], tags__caribbean=tags['caribbean'], tags__mexican=tags['mexican'], tags__spicy=tags['spicy'], tags__fine_food=tags['fine_food'], tags__kosher=tags['kosher'], tags__healthy=tags['healthy'], tags__vegan=tags['vegan'], tags__vegetarian=tags['vegetarian'],
                tags__gluten__free=tags['gluten_free'], tags__italian=tags['italian'], tags__middle_eastern=tags['middle_eastern'], tags__snack=tags['snack'], tags__thai=tags['thai'], tags__canadian=tags['canadian'], tags__vietnamese=tags['vietnamese'], tags__has_nuts=tags['has_nuts'], tags__lactose_free=tags['lactose_free'],
                tags__meat__bear=meat['bear'], tags__meat__beef=meat['beef'], tags__meat__buffalo=meat['buffalo'], tags__meat__calf=meat['calf'], tags__meat__caribou=meat['caribou'], tags__meat__goat=meat['goat'], tags__meat__ham=meat['ham'], tags__meat__horse=meat['horse'], tags__meat__kangaroo=meat['kangaroo'], tags__meat__lamb=meat['lamb'], tags__meat__moose=meat['moose'], tags__meat__mutton=meat['mutton'], tags__meat__opossum=meat['opossum'],
                tags__meat__pork=meat['pork'], tags__meat__bacon=meat['bacon'], tags__meat__rabbit=meat['rabbit'], tags__meat__snake=meat['snake'], tags__meat__squirrel=meat['squirrel'], tags__meat__turtle=meat['turtle'], tags__meat__veal=meat['veal'], tags__meat__chicken=meat['chicken'], tags__meat__hen=meat['hen'], tags__meat__duck=meat['duck'], tags__meat__goose=meat['goose'],
                tags__meat__ostrich=meat['ostrich'], tags__meat__quail=meat['quail'], tags__meat__turkey=meat['turkey'], tags__seafood__clam=seafood['clam'], tags__seafood__pangasius=seafood['pangasius'], tags__seafood__cod=seafood['cod'], tags__seafood__crab=seafood['crab'], tags__seafood__catfish=seafood['catfish'], tags__seafood__alaska_pollack=seafood['alaska_pollack'], tags__seafood__tilapia=seafood['tilapia'], tags__seafood__salmon=seafood['salmon'], tags__seafood__tuna=seafood['tuna'],
                tags__seafood__shrimp=seafood['shrimp'], tags__seafood__lobster=seafood['lobster'], tags__seafood___eel=seafood['eel'], tags__seafood__trout=seafood['trout'], tags__seafood__pike=seafood['pike'], tags__seafood__shark=seafood['shark'], meal_type__breakfast=meal_type['breakfast'], meal_type__lunch=meal_type['lunch'], meal_type__dinner=meal_type['dinner'])
                add_food_item.save()
            except Exception as e:
                return("Error \n %s" % (e))
            new_food_item_id = str(add_food_item.id)
            return({'image_id': new_food_item_id})
        else:
            return('Could not authenticate')

    def extract_food_tags(self, tags, meat, seafood):
        tags = {}
        pass

    def get_food_by_tags(self, tags):
        pass

    def get_restaurant_id_by_api_token(self, api_token):
        valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if (len(valid_token) > 0):
            restaurant_id = valid_token[0].id
            return(restaurant_id)
        else:
            return(None)

    def get_food_items_by_restaurant_id(self, restaurant_id, api_token):
        if self.check_valid_api_token(api_token) == True:
            try:
                foods_by_restaurant = Zatiq_Food_Items.objects(restaurant_id=restaurant_id)
            except Exception as e:
                return("Error \n %s" % (e))
            if len(foods_by_restaurant) > 0:
                food_items_dict = self.generate_food_items_dict(foods_by_restaurant)
                
    def check_valid_api_token(self, api_token):
        valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if len(valid_token) > 0:
            return(True)
        else:
            return(False)

    def generate_food_items_dict(self, food_items):
        food_items_dict = {}
        for food_item in range(len(food_items)):
            restaurant_id = food_items[food_item].restaurant_id
            item_name = food_items[food_item].item_name
            overview = food_items[food_item].overview
            image = food_items[food_item].image
            image_aspect_ratio = food_items[food_item].image_aspect_ratio
            tags = food_items[food_item].overview
            photo_info = {'image_id': image_id, 'base64': base64, 'image_aspect_ratio': image_aspect_ratio}
            food_items_dict[photo] = photo_info
        return(food_items_dict)

    def generate_food_items_tags_dict(self, tags):
        tags_dict = {}
        for tag in range(len(tags)):
            pass
