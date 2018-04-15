from mongoengine import *

class Zatiq_Business_Hours(EmbeddedDocument):
    monday_start = StringField(required=True)
    monday_end = StringField(required=True)
    tuesday_start = StringField(required=True)
    tuesday_end = StringField(required=True)
    wednesday_start = StringField(required=True)
    wednesday_end = StringField(required=True)
    thursday_start = StringField(required=True)
    thursday_end = StringField(required=True)
    friday_start = StringField(required=True)
    friday_end = StringField(required=True)
    saturday_start = StringField(required=True)
    saturday_end = StringField(required=True)
    sunday_start = StringField(required=True)
    sunday_end = StringField(required=True)
