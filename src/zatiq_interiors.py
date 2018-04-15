from mongoengine import *
from zatiq_businesses import Zatiq_Businesses
import datetime

class Zatiq_Interiors(Document):
    restaurant_id = ReferenceField(Zatiq_Businesses, reverse_delete_rule=CASCADE)
    image = StringField(required=True)
    image_aspect_ratio = StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)