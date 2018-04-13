from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items

class ZatiqFoodItemsMongoDBClient(object):
    def add_food_item(self, restaurant_id, image, image_aspect_ratio, overview, item_name):
        add_food_item = Zatiq_Food_Items(restaurant_id=restaurant_id, item_name=item_name, image=image, image_aspect_ratio=image_aspect_ratio, overview=overview).save()
        check_food_items = Zatiq_Food_Items.objects(restaurant_id=restaurant_id).to_json()
        print(check_food_items)
        return(check_food_items)

    def get_food_by_tags(self, tags):
        pass

    def get_food_by_id(self):
        pass