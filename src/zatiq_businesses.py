from mongoengine import *
import datetime
from zatiq_business_hours import Zatiq_Business_Hours

class Zatiq_Businesses(Document):
    business_email = StringField(required=True)
    business_password = BinaryField(required=True)
    business_name = StringField(required=True)
    website = StringField(required=True)
    address = StringField(required=True)
    number = StringField(required=True)
    image = StringField(required=True)
    image_aspect_ratio = StringField(required=True)
    zatiq_token = StringField(required=True)
    hours = EmbeddedDocumentField(Zatiq_Business_Hours)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    date_modified = DateTimeField(default=datetime.datetime.utcnow)
    price_range = StringField(required=False)
    average_food_rating = StringField(required=False)
    delivery = BooleanField(required=True)
    takeout = BooleanField(required=True)
    reservation = BooleanField(required=True)
    patio = BooleanField(required=True)
    wheelchair_accessible = BooleanField(required=True)
