from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_deal_items import Zatiq_Deal_Items
from requests import post
import os

class ZatiqDealsMongoDBClient(object):
    def save_image_to_db(self, imagedata, food_item_id):
        if not imagedata:
            return "Error! No imagedata provided to save_image_to_db function"
        
        image_url = post("http://167.99.177.29:5000/upload/", json={'imagedata': imagedata})
        if 'Error' in image_url:
            return "Error! Invalid image provided"

        try:
            add_zatiq_deal = Zatiq_Deal_Items(food_item_id=food_item_id, image=image_url).save()
        except Exception as e:
            return("Error \n %s" % (e))
        return {"status": "Zatiq Promotion Added"}

    def get_list_of_food_items(self):
        food_items_names_dict = {}

        try:
            food_items = Zatiq_Food_Items.objects()
        except Exception as e:
            return("Error \n %s" % (e))

        if len(food_items) > 0:
            for food_item_name in range(len(food_items)):
                food_items_names_dict[str(food_items[food_item_name].item_name)] = str(food_items[food_item_name].id)
        
        return food_items_names_dict