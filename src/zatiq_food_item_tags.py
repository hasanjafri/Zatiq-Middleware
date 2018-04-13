from mongoengine import *
from zatiq_meat_types import Zatiq_Meat_Types
from zatiq_sea_food_types import Zatiq_Sea_Food_Types

class Zatiq_Food_Item_Tags(EmbeddedDocument):
    breakfast = BooleanField(default=False)
    brunch = BooleanField(default=False)
    lunch = BooleanField(default=False)
    indian = BooleanField(default=False)
    greek = BooleanField(default=False)
    chinese = BooleanField(default=False)
    japanese = BooleanField(default=False)
    korean = BooleanField(default=False)
    sushi = BooleanField(default=False)
    dessert = BooleanField(default=False)
    burger = BooleanField(default=False)
    pizza = BooleanField(default=False)
    fast_food = BooleanField(default=False)
    halal = BooleanField(default=False)
    cheap = BooleanField(default=False)
    caribbean = BooleanField(default=False)
    mexican = BooleanField(default=False)
    spicy = StringField(default='0')
    fine_food = BooleanField(default=False)
    kosher = BooleanField(default=False)
    healthy = BooleanField(default=False)
    vegan = BooleanField(default=False)
    vegetarian = BooleanField(default=False)
    gluten_free = BooleanField(default=False)
    italian = BooleanField(default=False)
    middle_eastern = BooleanField(default=False)
    snack = BooleanField(default=False)
    thai = BooleanField(default=False)
    canadian = BooleanField(default=False)
    vietnamese = BooleanField(default=False)
    dinner = BooleanField(default=False)
    has_nuts = BooleanField(default=False)
    lactose_free = BooleanField(default=False)
    meat_type = EmbeddedDocumentField(Zatiq_Meat_Types)
    sea_food_type = EmbeddedDocumentField(Zatiq_Sea_Food_Types)