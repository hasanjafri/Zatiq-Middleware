from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_deal_items import Zatiq_Deal_Items
from zatiq_users import Zatiq_Users
from zatiq_businesses import Zatiq_Businesses
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
            add_zatiq_deal = Zatiq_Deal_Items(food_item_id=food_item_id, image=image_url.text).save()
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

    def get_all_deals(self, api_token):
        if self.check_valid_api_token(api_token) == True:
            try:
                zatiq_deals = Zatiq_Deal_Items.objects()
            except Exception as e:
                return("Error \n %s" % (e))

            if len(zatiq_deals) > 0:
                deals_response = self.generate_deals_dict(zatiq_deals)
                return(deals_response)
            else:
                return([])
        else:
            return("Could not authenticate")

    def generate_deals_dict(self, zatiq_deals):
        deals_list = []
        for deal in range(len(zatiq_deals)):
            image = zatiq_deals[deal].image
            food_item_id = zatiq_deals[deal].food_item_id
            deal_info = {'image': "http://167.99.177.29:5000/image/"+str(image), food_item_id: str(food_item_id)}
            deals_list.append(deal_info)
        return(deals_list)

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