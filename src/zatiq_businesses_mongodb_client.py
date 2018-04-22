from mongoengine import *
import secrets
from simplecrypt import encrypt, decrypt
from config import secret
from zatiq_businesses import Zatiq_Businesses
from zatiq_menus import Zatiq_Menus
from zatiq_interiors import Zatiq_Interiors
from zatiq_reviews import Zatiq_Reviews

class ZatiqBusinessesMongoDBClient(object):
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

    def get_restaurant_id_by_api_token(self, api_token):
        valid_token = Zatiq_Businesses.objects(zatiq_token=api_token)
        if (len(valid_token) > 0):
            restaurant_id = valid_token[0].id
            return(restaurant_id)
        else:
            return(None)

    def generate_reviews_list(self, reviews):
        reviews_list = []
        for review in reviews:
            restaurant_name = self.get_business_name_by_id(reviews[review].restaurant_id)
            restaurant_id = reviews[review].restaurant_id
            food_item_name = self.get_food_name_by_id(reviews[review].food_item_id)
            food_item_id = reviews[review].food_item_id
            text = reviews[review].text
            image = {'base64': reviews[review].image, 'image_aspect_ratio': reviews[review].image_aspect_ratio}
            rating = reviews[review].rating
            date_created = reviews[review].date_created
            review_info = {'restaurant_id': str(restaurant_id), 'restaurant_name': restaurant_name, 'food_item_id': food_item_id,
                'food_item_name': food_item_name, 'text': text, 'image': image, 'rating': rating, 'date_created': date_created}
            reviews_list.append(review_info)
        return(reviews_list)

    def get_all_reviews(self, api_token):
        if not api_token:
            return('Could not authenticate')

        if self.check_valid_api_token(api_token) == True:
            restaurant_id = self.get_restaurant_id_by_api_token(api_token)
            try:
                all_reviews = Zatiq_Reviews.objects(restaurant_id=restaurant_id)
            except Exception as e:
                return("Error \n %s" % (e))

            if len(all_reviews) > 0:   
                reviews_list = self.generate_reviews_list(all_reviews)
                return(reviews_list)
            else:
                return('No reviews found for business')
        else:
            return('Could not authenticate')
    
    def upload_menu_photo(self, image, image_aspect_ratio, api_token):
        if self.check_valid_api_token(api_token) == True:
            restaurant = self.get_restaurant_id_by_api_token(api_token)
            if restaurant != None:
                try:
                    new_menu_photo = Zatiq_Menus(restaurant_id=restaurant, image=image, image_aspect_ratio=image_aspect_ratio)
                    new_menu_photo.save()
                except Exception as e:
                    return("Error \n %s" % (e))
                image_id = str(new_menu_photo.id)
                return({'image_id': image_id})
            else:
                return('An error occurred')
    
    def delete_menu_photo(self, image_id, api_token):
        if self.check_valid_api_token(api_token) == True:
            Zatiq_Menus.objects(id=image_id).delete()
            return('Image deleted')
        else:
            return('An error occurred')

    def get_menu_photos_by_restaurant(self, api_token):
        if self.check_valid_api_token(api_token) == True:
            restaurant = Zatiq_Businesses.objects(zatiq_token=api_token)[0].id
            menu_photos = Zatiq_Menus.objects(restaurant_id=restaurant)
            result = self.generate_photos_dict(menu_photos)
            return(result)

    def generate_photos_dict(self, photos):
        photos_list = []
        for photo in range(len(photos)):
            image_id = str(photos[photo].id)
            base64 = photos[photo].image
            image_aspect_ratio = photos[photo].image_aspect_ratio
            photo_info = {'image_id': image_id, 'image': {'base64': base64, 'image_aspect_ratio': image_aspect_ratio}}
            photos_list.append(photo_info)
        return(photos_list)

    def upload_interior_photo(self, image, image_aspect_ratio, api_token):
        if self.check_valid_api_token(api_token) == True:
            restaurant = self.get_restaurant_id_by_api_token(api_token)
            if restaurant != None:
                try:
                    new_interior_photo = Zatiq_Interiors(restaurant_id=restaurant, image=image, image_aspect_ratio=image_aspect_ratio)
                    new_interior_photo.save()
                except Exception as e:
                    return("Error \n %s" % (e))
                image_id = str(new_interior_photo.id)
                return({'image_id': image_id})
            else:
                return('An error occurred')

    def delete_interior_photo(self, image_id, api_token):
        if self.check_valid_api_token(api_token) == True:
            Zatiq_Interiors.objects(id=image_id).delete()
            return('Image deleted')
        else:
            return('An error occurred')

    def get_interior_photos_by_restaurant(self, api_token):
        if self.check_valid_api_token(api_token) == True:
            restaurant = Zatiq_Businesses.objects(zatiq_token=api_token)[0].id
            interior_photos = Zatiq_Interiors.objects(restaurant_id=restaurant)
            result = self.generate_photos_dict(interior_photos)
            return(result)
    
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
        
        if self.check_valid_api_token(api_token) == True:
            get_business_info = Zatiq_Businesses.objects(zatiq_token=api_token)
            email = get_business_info[0].business_email
            name = get_business_info[0].business_name
            website = get_business_info[0].website
            address = get_business_info[0].address
            number = get_business_info[0].number
            image = {'base64': get_business_info[0].image, 'image_aspect_ratio': get_business_info[0].image_aspect_ratio}
            api_token = get_business_info[0].zatiq_token
            delivery = get_business_info[0].delivery
            takeout = get_business_info[0].takeout
            reservation = get_business_info[0].reservation
            patio = get_business_info[0].patio
            wheelchair_accessible = get_business_info[0].wheelchair_accessible
            hours = self.generate_business_hours(get_business_info[0].hours)
            return([email, name, website, address, number, image, api_token, hours, delivery, takeout, reservation, patio, wheelchair_accessible])
        else:
            return('Could not authenticate')

    def update_business_profile(self, api_token, hours, name, address, website, number, image, image_aspect_ratio, features):
        if self.check_valid_api_token(api_token) == True:
            try:
                Zatiq_Businesses.objects(zatiq_token=api_token).update_one(upsert=False,
                set__business_name=name, set__address=address, set__website=website, set__number=number, set__image=image, set__image_aspect_ratio=image_aspect_ratio,
                set__hours__monday_start=hours['start']['monday'], set__hours__monday_end=hours['end']['monday'],
                set__hours__tuesday_start=hours['start']['tuesday'], set__hours__tuesday_end=hours['end']['tuesday'],
                set__hours__wednesday_start=hours['start']['wednesday'], set__hours__wednesday_end=hours['end']['wednesday'],
                set__hours__thursday_start=hours['start']['thursday'], set__hours__thursday_end=hours['end']['thursday'],
                set__hours__friday_start=hours['start']['friday'], set__hours__friday_end=hours['end']['friday'],
                set__hours__saturday_start=hours['start']['saturday'], set__hours__saturday_end=hours['end']['saturday'],
                set__hours__sunday_start=hours['start']['sunday'], set__hours__sunday_end=hours['end']['sunday'], set__delivery=features['delivery'],
                set__takeout=features['takeout'], set__reservation=features['reservation'], set__patio=features['patio'], set__wheelchair_accessible=features['wheelChair'])
            except Exception as e:
                return("Error \n %s" % (e))
            zatiq_business = Zatiq_Businesses.objects(zatiq_token=api_token)
            if len(zatiq_business) > 0:
                new_name = zatiq_business[0].business_name
                new_image = zatiq_business[0].image
                new_image_aspect_ratio = zatiq_business[0].image_aspect_ratio
                api_token = zatiq_business[0].zatiq_token
            else:
                return('An error occurred')
            return([new_name, new_image, new_image_aspect_ratio, api_token])
        else:
            return('Could not authenticate')


    def business_logout(self, api_token):
        if not api_token:
            return('Could not authenticate')
        
        if self.check_valid_api_token(api_token) == True:
            logged_business = Zatiq_Businesses.objects(zatiq_token=api_token).update_one(upsert=False, set__zatiq_token='NULL')
            return('Logged out successfully')
        else:
            return('An error occurred')

    def business_login(self, business_email, business_password):
        if not business_email:
            return(['Please specify your email!'])
        if not business_password:
            return(['Please type your password!'])

        check_business_login = Zatiq_Businesses.objects(business_email=business_email)

        if len(check_business_login) > 0:
            encrypted_password = check_business_login[0].business_password
            if self.verify_password(business_password, encrypted_password) == True:
                new_api_token = self.generate_zatiq_api_token()
                try:
                    Zatiq_Businesses.objects(business_email=business_email).update_one(upsert=False, set__zatiq_token=new_api_token)
                except Exception as e:
                    return("Error \n %s" % (e))
                business_name = check_business_login[0].business_name
                image = check_business_login[0].image
                image_aspect_ratio = check_business_login[0].image_aspect_ratio
                return([business_name, new_api_token, image, image_aspect_ratio])
            else:
                return(['Incorrect Password!'])
        else:
            return(["No such email address!"])

    def business_register(self, business_email, business_password, hours, business_name, address, website, number, image, image_aspect_ratio, features):
        if not business_email:
            return(["Please specify your email"])
        if not business_password:
            return(["Please type in your password"])
        if not business_name:
            return(["Please enter your business name"])
        if not hours:
            return(["Please select your business hours"])

        check_business_register = Zatiq_Businesses.objects(business_email=business_email)
        if len(check_business_register) > 0:
            return(["Business is already registered with this email"])
        else:
            encrypted_password = self.encrypt_password(business_password)
            api_token = self.generate_zatiq_api_token()
            register_business = Zatiq_Businesses.objects(business_email=business_email).update_one(upsert=True,
             set__business_password=encrypted_password, set__zatiq_token=api_token, set__business_name=business_name, set__address=address, set__website=website, set__number=number, set__image=image, set__image_aspect_ratio=image_aspect_ratio,
             set__hours__monday_start=hours['start']['monday'], set__hours__monday_end=hours['end']['monday'],
             set__hours__tuesday_start=hours['start']['tuesday'], set__hours__tuesday_end=hours['end']['tuesday'],
             set__hours__wednesday_start=hours['start']['wednesday'], set__hours__wednesday_end=hours['end']['wednesday'],
             set__hours__thursday_start=hours['start']['thursday'], set__hours__thursday_end=hours['end']['thursday'],
             set__hours__friday_start=hours['start']['friday'], set__hours__friday_end=hours['end']['friday'],
             set__hours__saturday_start=hours['start']['saturday'], set__hours__saturday_end=hours['end']['saturday'],
             set__hours__sunday_start=hours['start']['sunday'], set__hours__sunday_end=hours['end']['sunday'], set__delivery=features['delivery'],
             set__takeout=features['takeout'], set__reservation=features['reservation'], set__patio=features['patio'], set__wheelchair_accessible=features['wheelChair'])
            return(self.business_login(business_email, business_password))
