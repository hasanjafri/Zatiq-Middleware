import boto3
import botocore
import secrets
import base64
import os

S3_BUCKET = 'zatiqbusiness-images'

class ZatiqAWSS3Client(object):
    def __init__(self):
        self.s3_client = boto3.client("s3", config=botocore.client.Config(signature_version='s3v4', region_name='ca-central-1'))

    def generate_unique_image_key(self):
        image_key = secrets.token_urlsafe(16)
        if self.check_image_key_exists(image_key) == False:
            return(''+image_key+'.png')

    def check_image_key_exists(self, key):
        check_unique_key = self.s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=key)
        if check_unique_key['KeyCount'] == 0:
            return(False)
        else:
            self.generate_unique_image_key()

    def save_b64_image(self, b64img):
        imgdata = base64.b64decode(b64img)
        file_name = "temp_food_pic.png"
        with open(file_name, 'wb') as f:
            f.write(imgdata)
        return('./'+file_name)

    def delete_temp_image(self, imagepath):
        try:
            os.remove(imagepath)
        except Exception as e:
            return("Error \n %s" % (e))

        if self.check_file_deleted(imagepath) == True:
            return(True)
        else:
            self.delete_temp_image(imagepath)

    def check_file_deleted(self, imagepath):
        if os.path.isfile(imagepath) == True:
            self.delete_temp_image(imagepath)
        else:
            return(True)

    def verify_upload_succeeded(self, key):
        check_object_exists = self.s3_client.list_objects_v2(Bucket=S3_BUCKET, Prefix=key)
        if check_object_exists['KeyCount'] >= 1:
            return(True)
        else:
            return(False)

    def upload_image_to_s3(self, b64str):
        unique_key = self.generate_unique_image_key()
        imagepath = self.save_b64_image(b64str)
        try:
            self.s3_client.upload_file(Filename=imagepath, Bucket=S3_BUCKET, Key=unique_key)
        except boto3.exceptions.S3UploadFailedError as e:
            return("Error \n %s" % (e))

        if self.verify_upload_succeeded(unique_key) == True:
            self.delete_temp_image(imagepath)
            url = self.s3_client.generate_presigned_url(ClientMethod='get_object', Params={'Bucket': S3_BUCKET, 'Key': unique_key})
            return(url)
        else:
            return("Upload failed")
