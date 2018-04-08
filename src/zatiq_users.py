from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
import datetime

class Zatiq_Users(Document):
    user_email = StringField(required=False)
    auth_token = StringField(required=True)
    user_name = StringField(required=True)
    zatiq_token = StringField(required=True)
    date_created = DateTimeField(default=datetime.datetime.utcnow)
    facebook_id = StringField()
    google_id = StringField()
    date_accessed = DateTimeField(default=datetime.datetime.utcnow)
    last_eaten = ListField(ReferenceField(Zatiq_Food_Items))