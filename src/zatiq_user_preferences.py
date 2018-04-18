from mongoengine import *
from zatiq_meat_types import Zatiq_Meat_Types
from zatiq_sea_food_types import Zatiq_Sea_Food_Types

class Zatiq_User_Preferences(EmbeddedDocument):
    halal = BooleanField(required=True)
    spicy = BooleanField(required=True)
    kosher = BooleanField(required=True)
    healthy = BooleanField(required=True)
    vegan = BooleanField(required=True)
    vegetarian = BooleanField(required=True)
    gluten_free = BooleanField(required=True)
    nuts_allergy = BooleanField(required=True)
    lactose_intolerant = BooleanField(required=True)

