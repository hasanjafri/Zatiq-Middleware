from mongoengine import *
from zatiq_meat_types import Zatiq_Meat_Types
from zatiq_sea_food_types import Zatiq_Sea_Food_Types

class Zatiq_Business_Preferences(EmbeddedDocument):
    halal = BooleanField(required=True)
    spicy = BooleanField(required=True)
    kosher = BooleanField(required=True)
    healthy = BooleanField(required=True)
    vegan = BooleanField(required=True)
    vegetarian = BooleanField(required=True)
    gluten_free = BooleanField(required=True)
    lactose_free = BooleanField(required=True)
    milk_allergy = BooleanField(required=True)
    has_eggs = BooleanField(required=True)
    fish_allergy = BooleanField(required=True)
    crustacean_allergy = BooleanField(required=True)
    has_wheat = BooleanField(required=True)
    has_soybeans = BooleanField(required=True)
    jain = BooleanField(required=True)
    omnivore = BooleanField(required=True)
    pescatarian = BooleanField(required=True)
    has_peanuts = BooleanField(required=True)
    has_treenuts = BooleanField(required=True)