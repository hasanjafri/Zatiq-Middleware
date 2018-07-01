from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_businesses import Zatiq_Businesses
import random

class ZatiqGuestsClient(object):
    def get_guest_food_by_button(self, button):
        if button == 'promotions':
            try:
                food_items = Zatiq_Food_Items.objects.order_by('discount_price')
            except Exception as e:
                return("Error \n %s" % (e))

            if len(food_items) > 0:
                return(self.generate_food_items_dict(food_items))
            else:
                return([])

        elif button == 'top_picks':
            try:
                food_items = Zatiq_Food_Items.objects.order_by('-views')
            except Exception as e:
                return("Error \n %s" % (e))

            if len(food_items) > 0:
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
                food_items_dict = self.generate_food_items_dict(food_items)
                return(food_items_dict)  
            else:
                return([])

        else:
            return('Category not found')
        

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