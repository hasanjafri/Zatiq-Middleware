from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
from zatiq_user_preferences import Zatiq_User_Preferences
from zatiq_user_history import Zatiq_User_History
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
    preferences = EmbeddedDocumentField(Zatiq_User_Preferences)
    history = EmbeddedDocumentListField(Zatiq_User_History)

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.datetime.utcnow()
        self.date_accessed = datetime.datetime.utcnow()
        return(super(Zatiq_Users, self).save(*args, **kwargs))