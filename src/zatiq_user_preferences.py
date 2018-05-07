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
    lactose_intolerant = BooleanField(required=True)
    milk_allergy = BooleanField(required=True)
    eggs_allergy = BooleanField(required=True)
    fish_allergy = BooleanField(required=True)
    crustacean_allergy = BooleanField(required=True)
    wheat_allergy = BooleanField(required=True)
    soybeans_allergy = BooleanField(required=True)
    jain = BooleanField(required=True)
    omnivore = BooleanField(required=True)
    pescatarian = BooleanField(required=True)
    peanuts_allergy = BooleanField(required=True)
    treenuts_allergy = BooleanField(required=True)
