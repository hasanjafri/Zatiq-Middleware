from mongoengine import *
from zatiq_businesses import Zatiq_Businesses
from zatiq_food_items import Zatiq_Food_Items
from zatiq_users import Zatiq_Users
import datetime

class Zatiq_Reviews(Document):
   restaurant_id = ReferenceField(Zatiq_Businesses, reverse_delete_rule=2, dbref=True)
   food_item_id = ReferenceField(Zatiq_Food_Items, dbref=True)
   reviewer_id = ReferenceField(Zatiq_Users, reverse_delete_rule=2, dbref=True)
   text = StringField(required=True)
   image = BinaryField(required=False)
   rating = StringField(required=True, default='0.00')
   date_created = DateTimeField(default=datetime.datetime.utcnow)
