from mongoengine import *
import secrets
import json
from simplecrypt import encrypt, decrypt
from config import secret
from zatiq_businesses import Zatiq_Businesses
from zatiq_menus import Zatiq_Menus
from zatiq_interiors import Zatiq_Interiors

class ZatiqBusinessesMongoDBClient(object):
    def get_all_businesses(self):
        all_businesses = []
        for user in Zatiq_Businesses.objects:
            all_businesses.append(user.user_name)
        return(json.dumps(all_businesses))

    def get_specific_business(self, businessEmail):
        business = Zatiq_Businesses.objects(business_email=businessEmail)
        return(json.dumps(business[0].business_name))

    def generate_zatiq_api_token(self):
        api_token = secrets.token_urlsafe(32)
        if (self.check_api_token_exists(api_token) == False):
            return(api_token)
        else:
            self.generate_zatiq_api_token()

    def check_api_token_exists(self, api_token):
        check_api_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if len(check_api_token) > 0:
            self.generate_zatiq_api_token()
        else:
            return(False)

    def encrypt_password(self, password):
        encrypted_password = encrypt(secret, password.encode('utf-8'))
        return(encrypted_password)

    def verify_password(self, password, encrypted_password):
        decrypted_password = decrypt(secret, encrypted_password)
        password_str = decrypted_password.decode('utf-8')
        if password_str == password:
            return(True)
        else:
            return(False)

    def check_valid_api_token(self, api_token):
        valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if len(valid_token) > 0:
            return(True)
        else:
            return(False)
    
    def upload_menu_photo(self, image, image_aspect_ratio, api_token):
        if self.check_valid_api_token(api_token) == True:
            restaurant = Zatiq_Businesses.objects(zatiq_token=api_token)[0].id
            new_menu = Zatiq_Menus(restaurant_id=restaurant, image=image, image_aspect_ratio=image_aspect_ratio).save()
            return('Upload successful')
        else:
            return('An error occurred')

    def generate_menu_photos_dict(self, photos):
        menu_photos = {}
        for photo in photos:
            pass

    def get_menu_by_restaurant(self, api_token):
        if self.check_api_token_exists(api_token) == True:
            restaurant = Zatiq_Businesses.objects(zatiq_token=api_token)[0].id
            menu_photos = Zatiq_Menus.objects(restaurant_id=restaurant)
            pass

    def upload_interior_photo(self, image, image_aspect_ratio, api_token):
        if self.check_valid_api_token(api_token) == True:
            restaurant = Zatiq_Businesses.objects(zatiq_token=api_token)[0].id
            new_interior = Zatiq_Interiors(restaurant_id=restaurant, image=image, image_aspect_ratio=image_aspect_ratio).save()
            return('Upload successful')
        else:
            return('An error occurred')
    
    def generate_business_hours(self, business):
        hours_dict = {'start': {
            'monday': business.monday_start,
            'tuesday': business.tuesday_start,
            'wednesday': business.wednesday_start,
            'thursday': business.thursday_start,
            'friday': business.friday_start,
            'saturday': business.saturday_start,
            'sunday': business.sunday_start
        }, 'end': {
            'monday': business.monday_end,
            'tuesday': business.tuesday_end,
            'wednesday': business.wednesday_end,
            'thursday': business.thursday_end,
            'friday': business.friday_end,
            'saturday': business.saturday_end,
            'sunday': business.sunday_end
        }}
        return(hours_dict)

    def get_business_profile(self, api_token):
        if not api_token:
            return('Could not authenticate')
        
        if self.check_api_token_exists(api_token) == True:
            get_business_info = Zatiq_Businesses.objects(zatiq_token=api_token)
            email = get_business_info[0].business_email
            name = get_business_info[0].business_name
            website = get_business_info[0].website
            address = get_business_info[0].address
            number = get_business_info[0].number
            image = get_business_info[0].image
            image_aspect_ratio = get_business_info[0].image_aspect_ratio
            api_token = get_business_info[0].zatiq_token
            hours = self.generate_business_hours(get_business_info.hours)
            return([email, name, website, address, number, image, image_aspect_ratio, api_token, hours])

    def business_login(self, business_email, business_password):
        if not business_email:
            return('Please specify your email!')
        if not business_password:
            return('Please type your password!')

        check_business_login = Zatiq_Businesses.objects(business_email=business_email)

        if len(check_business_login) > 0:
            encrypted_password = check_business_login[0].business_password
            if self.verify_password(business_password, encrypted_password) == True:
                business_name = check_business_login[0].business_name
                api_token = check_business_login[0].zatiq_token
                image = check_business_login[0].image
                return([business_name, api_token, image])
            else:
                return('Incorrect Password!')
        else:
            return("No such email address!")

    def business_register(self, business_email, business_password, hours, business_name, address, website, number, image, image_aspect_ratio):
        if not business_email:
            return("Please specify your email")
        if not business_password:
            return("Please type in your password")
        if not business_name:
            return("Please enter your business name")
        if not hours:
            return("Please select your business hours")

        check_business_register = Zatiq_Businesses.objects(business_email=business_email)
        if len(check_business_register) > 0:
            return("Business is already registered with this email")
        else:
            encrypted_password = self.encrypt_password(business_password)
            api_token = self.generate_zatiq_api_token()
            register_business = Zatiq_Businesses.objects(business_email=business_email).update_one(upsert=True,
             set__business_password=encrypted_password, set__zatiq_token=api_token, set__business_name=business_name, set__address=address, set__website=website, set__number=number,
             set__hours__monday_start=hours['start']['monday'], set__hours__monday_end=hours['end']['monday'],
             set__hours__tuesday_start=hours['start']['tuesday'], set__hours__tuesday_end=hours['end']['tuesday'],
             set__hours__wednesday_start=hours['start']['wednesday'], set__hours__wednesday_end=hours['end']['wednesday'],
             set__hours__thursday_start=hours['start']['thursday'], set__hours__thursday_end=hours['end']['thursday'],
             set__hours__friday_start=hours['start']['friday'], set__hours__friday_end=hours['end']['friday'],
             set__hours__saturday_start=hours['start']['saturday'], set__hours__saturday_end=hours['end']['saturday'],
             set__hours__sunday_start=hours['start']['sunday'], set__hours__sunday_end=hours['end']['sunday'])
            return(self.business_login(business_email, business_password))
