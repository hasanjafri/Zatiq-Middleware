from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_businesses import Zatiq_Businesses

class ZatiqFoodItemsMongoDBClient(object):
    def add_food_item(self, restaurant_id, image, image_aspect_ratio, overview, item_name, api_token, meal_type, tags, item_price, bouffet_item, meat, seafood):
        if self.check_valid_api_token(api_token) == True:
            try:
                add_food_item = Zatiq_Food_Items(restaurant_id=restaurant_id, item_name=item_name, image=image, image_aspect_ratio=image_aspect_ratio, overview=overview, meal_type=meal_type, is_beverage=tags['is_beverage'], item_price=item_price, bouffet_item=bouffet_item,
                set__tags_indian=tags['indian'], set__tags_greek=tags['greek'], set__tags_chinese=tags['chinese'], set__tags_japanese=tags['japanese'], set__tags_korean=tags['korean'], set__tags_sushi=tags['sushi'], set__tags_dessert=tags['dessert'], set__tags_burger=tags['burger'], set__tags_pizza=tags['pizza'],
                set__tags_fast_food=tags['fast_food'], set__tags_halal=tags['halal'], set__tags_caribbean=tags['caribbean'], set__tags_mexican=tags['mexican'], set__tags_spicy=tags['spicy'], set__tags_fine_food=tags['fine_food'], set__tags_kosher=tags['kosher'], set__tags_healthy=tags['healthy'], set__tags_vegan=tags['vegan'], set__tags_vegetarian=tags['vegetarian'],
                set__tags_gluten_free=tags['gluten_free'], set__tags_italian=tags['italian'], set__tags_middle_eastern=tags['middle_eastern'], set__tags_snack=tags['snack'], set__tags_thai=tags['thai'], set__tags_canadian=tags['canadian'], set__tags_vietnamese=tags['vietnamese'], set__tags_has_nuts=tags['has_nuts'], set__tags_lactose_free=tags['lactose_free'],
                set__tags_meat__bear=meat['bear'], set__tags_meat__beef=meat['beef'], set__tags_meat__buffalo=meat['buffalo'], set__tags_meat__calf=meat['calf'], set__tags_meat__caribou=meat['caribou'], set__tags_meat__goat=meat['goat'], set__tags_meat__ham=meat['ham'], set__tags_meat__horse=meat['horse'], set__tags_meat__kangaroo=meat['kangaroo'], set__tags_meat__lamb=meat['lamb'], set__tags_meat__moose=meat['moose'], set__tags_meat__mutton=meat['mutton'], set__tags_meat__opossum=meat['opossum'],
                set__tags_meat__pork=meat['pork'], set__tags_meat__bacon=meat['bacon'], set__tags_meat__rabbit=meat['rabbit'], set__tags_meat__snake=meat['snake'], set__tags_meat__squirrel=meat['squirrel'], set__tags_meat__turtle=meat['turtle'], set__tags_meat__veal=meat['veal'], set__tags_meat__chicken=meat['chicken'], set__tags_meat__hen=meat['hen'], set__tags_meat_duck=meat['duck'], set__tags_meat__goose=meat['goose'],
                set__tags_meat__ostrich=meat['ostrich'], set__tags_meat_quail=meat['quail'], set__tags_meat__turkey=tags['turkey'], set__tags_seafood__clam=seafood['clam'], set__tags_seafood__pangasius=seafood['pangasius'], set__tags_seafood__cod=seafood['cod'], set__tags_seafood__crab=seafood['crab'], set__tags_seafood__catfish=seafood['catfish'], set__tags_seafood__alaska_pollack=seafood['alaska_pollack'], set__tags_seafood__tilapia=seafood['tilapia'], set__tags_seafood__salmon=seafood['salmon'], set__tags_seafood__tuna=seafood['tuna'],
                set__tags_seafood__shrimp=seafood['shrimp'], set__tags_seafood__lobster=seafood['lobster'], set__tags_seafood__eel=seafood['eel'], set__tags_seafood__trout=seafood['trout'], set__tags_seafood__pike=seafood['pike'], set__tags_seafood__shark=seafood['shark'], set__meal_type__breakfast=meal_type['breakfast'], set__meal_type__lunch=meal_type['lunch'], set__meal_type__dinner=meal_type['dinner'])
                add_food_item.save()
            except Exception as e:
                return("Error \n %s" % (e))
            new_food_item_id = str(add_food_item.id)
            return(new_food_item_id)
        else:
            return('Could not authenticate')

    def extract_food_tags(self, tags, meat, seafood):
        tags = {}
        pass

    def get_food_by_tags(self, tags):
        pass

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
