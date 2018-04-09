from mongoengine import *
import datetime

class Zatiq_Businesses(Document):
    business_email = StringField(required=True)
    business_password = BinaryField(required=True)
    business_name = StringField(required=True)
    has_set_information = BooleanField(default=False)
    zatiq_token = StringField(required=True)
    date_created = StringField(default=datetime.datetime.utcnow)
    date_modified = StringField(default=datetime.datetime.utcnow)
    price_range = StringField(required=True)