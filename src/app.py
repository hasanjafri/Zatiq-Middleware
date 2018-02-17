from flask import Flask
from zatiq_aws_client import ZatiqAWSClient
app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello World!')

@app.route('/image/business/')
def upload_business_image_to_s3():
    zatiq_aws = ZatiqAWSClient
    response = zatiq_aws.get_all_buckets()
    return(response)