from mongoengine import *
from zatiq_food_items import Zatiq_Food_Items
import datetime

class Zatiq_User_History(EmbeddedDocument):
    food_item_id = ReferenceField(Zatiq_Food_Items, reverse_delete_rule=CASCADE)
    date_created = DateTimeField(default=datetime.datetime.utcnow)