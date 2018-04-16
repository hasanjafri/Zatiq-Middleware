from mongoengine import *

class Zatiq_Meal_Types(Document):
    breakfast = BooleanField(required=True)
    lunch = BooleanField(required=True)
    dinner = BooleanField(required=True)