from mongoengine import *
from zatiq_businesses import Zatiq_Businesses
import datetime

class Zatiq_Interiors(Document):
    restaurant_id = ReferenceField(Zatiq_Businesses, reverse_delete_rule=CASCADE)
    image = ListField(StringField())
    image_aspect_ratio = ListField(StringField())
    date_created = DateTimeField(default=datetime.datetime.utcnow)