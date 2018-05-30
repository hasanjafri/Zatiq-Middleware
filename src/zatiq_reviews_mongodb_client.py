from mongoengine import *
from zatiq_reviews import Zatiq_Reviews
from zatiq_users import Zatiq_Users
from zatiq_businesses import Zatiq_Businesses
from zatiq_food_items import Zatiq_Food_Items

class ZatiqReviewsMongoDBClient(object):
    def check_valid_api_token(self, api_token):
        valid_token = Zatiq_Users.objects(zatiq_token=api_token)
        if len(valid_token) > 0:
            return(True)
        else:
            return(False)

    def get_business_name_by_id(self, business_id):
        try:
            business_name = Zatiq_Businesses.objects(id=business_id)
        except Exception as e:
            return("Error \n %s" % (e))
        return(business_name[0].business_name)
    
    def get_reviewer_id_by_api_token(self, api_token):
        try:
            valid_token = Zatiq_Users.objects(zatiq_token=api_token)
        except Exception as e:
            return("Error \n %s" % (e))
        if len(valid_token) > 0:
            return(valid_token[0].id)
        else:
            return(None)

    def get_food_name_by_id(self, food_id):
        try:
            food_name = Zatiq_Food_Items.objects(id=food_id)
        except Exception as e:
            return("Error \n %s" % (e))
        return(food_name[0].item_name)

    def add_review(self, restaurant_id, food_item_id, text, image, rating, image_aspect_ratio, api_token):
        if not restaurant_id:
            return("Please specify a restaurant for your review")
        if not food_item_id:
            return("Please select what you ate at the time of this review")
        if not api_token:
            return("Could not authenticate Zatiq API Key")
        if not text:
            return("Please enter a review")
        if not rating:
            return("You must select a rating out of 5 stars")

        if self.check_valid_api_token(api_token) == True:
            image_url = post("http://167.99.177.29:5000/upload/", data={'imagedata': image}).json()['response']
            if 'Error' in image_url:
                return("Invalid image provided")
            reviewer_id = self.get_reviewer_id_by_api_token(api_token)
            if reviewer_id != None:  
                try:
                    Zatiq_Reviews(restaurant_id=restaurant_id, reviewer_id=reviewer_id, food_item_id=food_item_id, text=text, rating=rating, image=image_url, image_aspect_ratio=image_aspect_ratio).save()
                except Exception as e:
                    return("Error \n %s" % (e))
                return("Review added")
            else:
                return("No reviewer found with that API token")
        else:
            return('Could not authenticate')

    def generate_reviews_list(self, reviews):
        reviews_list = []
        for review in range(len(reviews)):
            restaurant_name = self.get_business_name_by_id(reviews[review].restaurant_id.id)
            restaurant_id = reviews[review].restaurant_id
            food_item_name = self.get_food_name_by_id(reviews[review].food_item_id.id)
            food_item_id = reviews[review].food_item_id
            text = reviews[review].text
            image = {'base64': 'http://167.99.177.29:5000/image/'+reviews[review].image, 'image_aspect_ratio': reviews[review].image_aspect_ratio}
            rating = reviews[review].rating
            date_created = reviews[review].date_created
            review_info = {'restaurant_id': str(restaurant_id), 'restaurant_name': restaurant_name, 'food_item_id': str(food_item_id),
                'food_item_name': food_item_name, 'text': text, 'image': image, 'rating': rating, 'date_created': date_created}
            reviews_list.append(review_info)
        return(reviews_list)

    def get_all_reviews_by_reviewer_id(self, api_token):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            reviewer_id = self.get_reviewer_id_by_api_token(api_token)
            if reviewer_id != None:
                try:
                    reviews = Zatiq_Reviews.objects(reviewer_id=reviewer_id)
                except Exception as e:
                    return("Error \n %s" % (e))
                if len(reviews) > 0:
                    self_reviews_dict = self.generate_reviews_list(reviews)
                    return(self_reviews_dict)
                else:
                    return([])
            else:
                return([])
        else:
            return('Could not authenticate')


        
