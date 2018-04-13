from mongoengine import *
from zatiq_businesses import Zatiq_Businesses
from zatiq_food_item_tags import Zatiq_Food_Item_Tags
import datetime

class Zatiq_Food_Items(Document):
   restaurant_id = ReferenceField(Zatiq_Businesses, reverse_delete_rule=CASCADE)
   item_name = StringField(required=True)
   overview = StringField(required=True)
   image = StringField(required=True)
   image_aspect_ratio = StringField(required=True)
   tags = EmbeddedDocumentField(Zatiq_Food_Item_Tags)
   is_beverage = BooleanField(default=False)
   item_price = StringField(default='0.00')
   average_review = StringField(default='0.00')
   bouffet_item = BooleanField(default=False)
   date_created = DateTimeField(default=datetime.datetime.utcnow)

