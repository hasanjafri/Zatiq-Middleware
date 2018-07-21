from mongoengine import *
import datetime
from zatiq_food_items import Zatiq_Food_Items

class Zatiq_Deal_Items(Document):
    food_item_id = ReferenceField(Zatiq_Food_Items, reverse_delete_rule=CASCADE)
    image = StringField(required=True)
    image_aspect_ratio = StringField(required=True)
    item_name = StringField(required=True)
    item_price = DecimalField(precision=2, rounding='ROUND_HALF_UP', default=0.00)
