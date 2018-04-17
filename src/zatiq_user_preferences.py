from mongoengine import *
from zatiq_meat_types import Zatiq_Meat_Types
from zatiq_sea_food_types import Zatiq_Sea_Food_Types

class Zatiq_User_Preferences(EmbeddedDocument):
    halal = BooleanField(default=False)
    spicy = BooleanField(default=True)
    kosher = BooleanField(default=False)
    healthy = BooleanField(default=False)
    vegan = BooleanField(default=False)
    vegetarian = BooleanField(default=False)
    gluten_free = BooleanField(default=False)
    nuts_allergy = BooleanField(default=True)
    lactose_intolerant = BooleanField(default=False)

