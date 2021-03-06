from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_deal_items import Zatiq_Deal_Items
from zatiq_users import Zatiq_Users
from zatiq_businesses import Zatiq_Businesses
from requests import post
import os

class ZatiqDealsMongoDBClient(object):
    def save_deal_to_db(self, food_item_id):
        # if not imagedata:
        #     return "Error! No imagedata provided to save_image_to_db function"
        
        # image_url = post("http://167.99.177.29:5000/upload/", json={'imagedata': imagedata})
        # if 'Error' in image_url:
        #     return "Error! Invalid image provided"

        linked_food_info = self.get_linked_food_item_info(food_item_id)
        if len(linked_food_info) > 0:
            try:
                add_zatiq_deal = Zatiq_Deal_Items(food_item_id=food_item_id, image=linked_food_info[0], image_aspect_ratio=linked_food_info[1], item_name=linked_food_info[2], item_price=linked_food_info[3],
                                    restaurant_image=linked_food_info[4], restaurant_image_aspect_ratio=linked_food_info[5], restaurant_name=linked_food_info[6]).save()
            except Exception as e:
                return("Error \n %s" % (e))
            return {"status": "Zatiq Promotion Added"}

    def get_linked_food_item_info(self, food_item_id):
        try:
            food_item_info = Zatiq_Food_Items.objects(id=food_item_id)
        except Exception as e:
            return("Error \n %s" % (e))

        if len(food_item_info) > 0:
            image = food_item_info[0].image
            image_aspect_ratio = food_item_info[0].image_aspect_ratio
            item_name = food_item_info[0].item_name
            item_price = food_item_info[0].item_price
            try:
                restaurant_info = Zatiq_Businesses.objects(id=food_item_info[0].restaurant_id.id)
            except Exception as e:
                return("Error \n %s" % (e))

            restaurant_image = restaurant_info[0].image
            restaurant_image_aspect_ratio = restaurant_info[0].image_aspect_ratio
            restaurant_name = restaurant_info[0].business_name

            return [image, image_aspect_ratio, item_name, item_price, restaurant_image, restaurant_image_aspect_ratio, restaurant_name]
        else:
            return []

    def delete_deal_from_db(self, deal_id):
        if not deal_id:
            return "Error! No deal specified to delete"

        #local_image_path = Zatiq_Deal_Items.objects(id=deal_id)[0].image
        try:
            Zatiq_Deal_Items(id=deal_id).delete()
        except Exception as e:
            return("Error \n %s" % (e))

        #delete_image_locally = post("http://167.99.177.29:5000/delete/", json={'imagepath': local_image_path})
        # if 'Error' in delete_image_locally:
        #     with open('./deal_delete_failed.txt', 'a') as file:
        #         file.write('(deal_id: {})\n'.format(deal_id))
        return {"status": "Zatiq deal deleted with id "+str(deal_id)+". Please refresh your page to see updated list of deals."}

    def get_list_of_food_items(self):
        food_items_names_dict = {}

        try:
            food_items = Zatiq_Food_Items.objects()
        except Exception as e:
            return("Error \n %s" % (e))

        if len(food_items) > 0:
            restaurant_names = self.get_all_restaurant_names(food_items)
            for food_item_name in range(len(food_items)):
                food_items_names_dict[str(food_items[food_item_name].item_name)+" ("+str(restaurant_names[food_item_name])+")"] = str(food_items[food_item_name].id)
        
        return food_items_names_dict

    def get_all_restaurant_names(self, food_items):
        restaurant_names_list = []
        for food_item in range(len(food_items)):
            try:
                restaurant_name = Zatiq_Businesses.objects(id=food_items[food_item].restaurant_id.id)
            except Exception as e:
                return("Error \n %s" % (e))

            restaurant_names_list.append(restaurant_name[0].business_name)
        return restaurant_names_list

    def get_all_deals(self):
        try:
            zatiq_deals = Zatiq_Deal_Items.objects()
        except Exception as e:
            return("Error \n %s" % (e))

        if len(zatiq_deals) > 0:
            deals_response = self.generate_deals_dict(zatiq_deals)
            return(deals_response)
        else:
            return([])

    def generate_deals_dict(self, zatiq_deals):
        deals_list = []
        for deal in range(len(zatiq_deals)):
            food_item_id = zatiq_deals[deal].food_item_id.id
            image = zatiq_deals[deal].image
            image_aspect_ratio = zatiq_deals[deal].image_aspect_ratio
            item_name = zatiq_deals[deal].item_name
            item_price = zatiq_deals[deal].item_price
            restaurant_image = zatiq_deals[deal].restaurant_image
            restaurant_image_aspect_ratio = zatiq_deals[deal].restaurant_image_aspect_ratio
            deal_info = {'image': "http://167.99.177.29:5000/image/"+str(image), 'food_item_id': str(food_item_id), 'item_name': str(item_name), 'item_price': str(item_price), 'image_aspect_ratio': str(image_aspect_ratio), 'restaurant_image': "http://167.99.177.29:5000/image/"+str(restaurant_image), 'restaurant_image_aspect_ratio': str(restaurant_image_aspect_ratio)}
            deals_list.append(deal_info)
        return(deals_list)

    def get_organized_remove_deals(self):
        try:
            zatiq_deals = Zatiq_Deal_Items.objects()
        except Exception as e:
            return("Error \n %s" % (e))

        if len(zatiq_deals) > 0:
            deals_dict = {}
            for deal in range(len(zatiq_deals)):
                deals_dict[str(zatiq_deals[deal].item_name)+" ("+str(zatiq_deals[deal].restaurant_name)+")"] = str(zatiq_deals[deal].id)
            return deals_dict
        else:
            return {}