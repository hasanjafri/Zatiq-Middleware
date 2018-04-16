from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_businesses import Zatiq_Businesses

class ZatiqFoodItemsMongoDBClient(object):
    def add_food_item(self, image, overview, item_name, api_token, meal_type, tags, item_price, meat, seafood):
        if self.check_valid_api_token(api_token) == True:
            restaurant = self.get_restaurant_id_by_api_token(api_token)
            try:
                add_food_item = Zatiq_Food_Items(restaurant_id=restaurant, item_name=item_name, image=image['base64'], image_aspect_ratio=image['image_aspect_ratio'], overview=overview, is_beverage=tags['is_beverage'], item_price=item_price,
                tags_indian=tags['indian'], tags_greek=tags['greek'], tags_chinese=tags['chinese'], tags_japanese=tags['japanese'], tags_korean=tags['korean'], tags_sushi=tags['sushi'], tags_dessert=tags['dessert'], tags_burger=tags['burger'], tags_pizza=tags['pizza'],
                tags_fast_food=tags['fast_food'], tags_halal=tags['halal'], tags_caribbean=tags['caribbean'], tags_mexican=tags['mexican'], tags_spicy=tags['spicy'], tags_fine_food=tags['fine_food'], tags_kosher=tags['kosher'], tags_healthy=tags['healthy'], tags_vegan=tags['vegan'], tags_vegetarian=tags['vegetarian'],
                tags_gluten_free=tags['gluten_free'], tags_italian=tags['italian'], tags_middle_eastern=tags['middle_eastern'], tags_snack=tags['snack'], tags_thai=tags['thai'], tags_canadian=tags['canadian'], tags_vietnamese=tags['vietnamese'], tags_has_nuts=tags['has_nuts'], tags_lactose_free=tags['lactose_free'],
                tags_meat_bear=meat['bear'], tags_meat_beef=meat['beef'], tags_meat_buffalo=meat['buffalo'], tags_meat_calf=meat['calf'], tags_meat_caribou=meat['caribou'], tags_meat_goat=meat['goat'], tags_meat_ham=meat['ham'], tags_meat_horse=meat['horse'], tags_meat_kangaroo=meat['kangaroo'], tags_meat_lamb=meat['lamb'], tags_meat_moose=meat['moose'], tags_meat_mutton=meat['mutton'], tags_meat_opossum=meat['opossum'],
                tags_meat_pork=meat['pork'], tags_meat_bacon=meat['bacon'], tags_meat_rabbit=meat['rabbit'], tags_meat_snake=meat['snake'], tags_meat_squirrel=meat['squirrel'], tags_meat_turtle=meat['turtle'], tags_meat_veal=meat['veal'], tags_meat_chicken=meat['chicken'], tags_meat_hen=meat['hen'], tags_meat_duck=meat['duck'], tags_meat_goose=meat['goose'],
                tags_meat_ostrich=meat['ostrich'], tags_meat_quail=meat['quail'], tags_meat_turkey=meat['turkey'], tags_seafood_clam=seafood['clam'], tags_seafood_pangasius=seafood['pangasius'], tags_seafood_cod=seafood['cod'], tags_seafood_crab=seafood['crab'], tags_seafood_catfish=seafood['catfish'], tags_seafood_alaska_pollack=seafood['alaska_pollack'], tags_seafood_tilapia=seafood['tilapia'], tags_seafood_salmon=seafood['salmon'], tags_seafood_tuna=seafood['tuna'],
                tags_seafood_shrimp=seafood['shrimp'], tags_seafood_lobster=seafood['lobster'], tags_seafood_eel=seafood['eel'], tags_seafood_trout=seafood['trout'], tags_seafood_pike=seafood['pike'], tags_seafood_shark=seafood['shark'], meal_type__breakfast=meal_type['breakfast'], meal_type__lunch=meal_type['lunch'], meal_type__dinner=meal_type['dinner'])
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
