from mongoengine import *
from zatiq_businesses import Zatiq_Businesses
from zatiq_food_items import Zatiq_Food_Items
from zatiq_users import Zatiq_Users
import datetime

class Zatiq_Reviews(Document):
   restaurant_id = ReferenceField(Zatiq_Businesses, reverse_delete_rule=CASCADE)
   food_item_id = ReferenceField(Zatiq_Food_Items)
   reviewer_id = ReferenceField(Zatiq_Users)
   text = StringField(required=True)
   image = StringField(required=True)
   image_aspect_ratio = StringField(required=True)
   rating = StringField(required=True, default='0.00')
   date_created = DateTimeField(default=datetime.datetime.utcnow)
