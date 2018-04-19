from mongoengine import *

class Zatiq_Meal_Types(EmbeddedDocument):
    breakfast = BooleanField(required=True)
    brunch = BooleanField(required=True)
    lunch = BooleanField(required=True)
    dinner = BooleanField(required=True)