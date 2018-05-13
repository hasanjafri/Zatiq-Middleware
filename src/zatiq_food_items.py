from mongoengine import *
from zatiq_businesses import Zatiq_Businesses
from zatiq_food_item_tags import Zatiq_Food_Item_Tags
from zatiq_meal_types import Zatiq_Meal_Types
import datetime

class Zatiq_Food_Items(Document):
   restaurant_id = ReferenceField(Zatiq_Businesses, reverse_delete_rule=CASCADE)
   item_name = StringField(required=True)
   overview = StringField(required=True)
   image = StringField(required=True)
   meal_type = EmbeddedDocumentField(Zatiq_Meal_Types)
   image_aspect_ratio = StringField(required=True)
   tags = EmbeddedDocumentField(Zatiq_Food_Item_Tags)
   is_beverage = BooleanField(default=False)
   calories = StringField(required=True)
   item_price = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=0.00)
   discount_price = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=0.00)
   average_review = StringField(default='0.00')
   bouffet_item = BooleanField(default=False)
   date_created = DateTimeField(default=datetime.datetime.utcnow)
   views = IntField(default=1)

   meta = {'indexes': [
       {'fields': ['$item_name', '$overview'],
        'default_language': 'english',
        'weights': {'item_name': 10, 'overview': 2}}
   ]}

