from mongoengine import *

class Zatiq_Sea_Food_Types(EmbeddedDocument):
   clam = BooleanField(default=False)
   pangasius = BooleanField(default=False)
   cod = BooleanField(default=False)
   crab = BooleanField(default=False)
   catfish = BooleanField(default=False)
   alaska_pollack = BooleanField(default=False)
   tilapia = BooleanField(default=False)
   salmon = BooleanField(default=False)
   tuna = BooleanField(default=False)
   shrimp = BooleanField(default=False)
   lobster = BooleanField(default=False)
   eel = BooleanField(default=False)
   trout = BooleanField(default=False)
   pike = BooleanField(default=False)
   shark = BooleanField(default=False)