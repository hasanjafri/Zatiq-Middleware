from mongoengine import *
import datetime
from zatiq_business_hours import Zatiq_Business_Hours
from zatiq_business_preferences import Zatiq_Business_Preferences

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
    date_accessed = DateTimeField(default=datetime.datetime.utcnow)
    price_range = StringField(required=False)
    average_food_rating = StringField(required=False)
    delivery = BooleanField(required=True)
    takeout = BooleanField(required=True)
    reservation = BooleanField(required=True)
    patio = BooleanField(required=True)
    parking = BooleanField(required=True)
    buffet = BooleanField(required=True)
    family_friendly = BooleanField(required=True)
    pescetarian_friendly = BooleanField(required=True)
    wifi = BooleanField(required=True)
    wheelchair_accessible = BooleanField(required=True)
    view_count = IntField(default=0)
    preferences = EmbeddedDocumentField(Zatiq_Business_Preferences)

    meta = {'indexes': [
        {'fields': ['$business_name', '$website'],
         'default_language': 'english',
         'weights': {'business_name': 10, 'website': 2}}
    ]}

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.datetime.utcnow()
        self.date_accessed = datetime.datetime.utcnow()
        return(super(Zatiq_Businesses, self).save(*args, **kwargs))
