from mongoengine import *
from zatiq_businesses import Zatiq_Businesses
import datetime

class Zatiq_Food_Items(Document):
   restaurant_id = ReferenceField(Zatiq_Businesses, reverse_delete_rule=CASCADE)
   item_name = StringField(required=True)
   is_halal = BooleanField(default=False)
   overview = StringField(required=True)
   image = StringField(required=True)
   image_aspect_ratio = StringField(required=True)
   cuisine_type = ListField(StringField(), default=['none'])
   dessert_item = BooleanField(default=False)
   vegan_friendly = BooleanField(default=False)
   breakfast_item = BooleanField(default=False)
   lunch_item = BooleanField(default=False)
   dinner_item = BooleanField(default=False)
   is_beverage = BooleanField(default=False)
   lactose_free = BooleanField(default=False)
   has_nuts = BooleanField(default=False)
   item_price = StringField(default='0.00')
   average_review = StringField(default='0.00')
   bouffet_item = BooleanField(default=False)
   meat_type = ListField(StringField(), default=['none'])
   seafood_type = ListField(StringField(), default=['none'])
   date_created = DateTimeField(default=datetime.datetime.utcnow)

