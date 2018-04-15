from mongoengine import *
import json
from zatiq_reviews import Zatiq_Reviews
from zatiq_users import Zatiq_Users

class ZatiqReviewsMongoDBClient(object):
    def get_all_reviews_by_reviewer_id(self, api_token):
        if self.check_valid_api_token(api_token) == True:
            all_reviews = []
            for review in Zatiq_Reviews.objects:
                all_reviews.append(review.reviewer_id)
            return(json.dumps(all_reviews))
        else:
            return('Could not authenticate Zatiq API Key')

    def check_valid_api_token(self, api_token):
        valid_token = Zatiq_Users.objects(zatiq_token=api_token)
        if len(valid_token) > 0:
            return(True)
        else:
            return(False)

    def get_reviews_by_restaurant_id(self, restaurant_id, api_token):
        get_all_reviews = Zatiq_Reviews.objects(restaurant_id=restaurant_id).to_json()
        check_business
        return(get_all_reviews)

    def add_review(self, restaurant_id, reviewer_id, food_item_id, text, image, rating, image_aspect_ratio, api_token):
        if not restaurant_id:
            return("Please specify a restaurant for your review")
        if not reviewer_id:
            return("Could not authenticate")
        if not food_item_id:
            return("Please select what you ate at the time of this review")
        if not api_token:
            return("Could not authenticate Zatiq API Key")
        if not text:
            return("Please enter a review")
        if not rating:
            return("You must select a rating out of 5 stars")

        if self.check_valid_api_token(api_token) == True:
            add_review = Zatiq_Reviews(restaurant_id=restaurant_id, reviewer_id=reviewer_id, food_item_id=food_item_id, text=text, rating=rating, image=image, image_aspect_ratio=image_aspect_ratio).save()
            get_all_reviews = self.get_reviews_by_restaurant_id(restaurant_id)
            return(get_all_reviews)
        

        
