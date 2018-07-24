import os

# S3_BUCKET = os.environ.get("S3_BUCKET_NAME")
# S3_KEY = os.environ.get("S3_ACCESS_KEY")
# S3_SECRET = os.environ.get("S3_SECRET_ACCESS_KEY")
# S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
secret = 'SDZoRP36tEQiFz-dkmGSK8Ju23JjD_rJ5wCwE6Vg5QE'

admin_username = os.environ.get('ADMIN_USERNAME')
admin_password = os.environ.get('ADMIN_PASSWORD')

SECRET_KEY = os.urandom(32)
DEBUG = True
PORT = 5000
