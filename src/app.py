from flask import Flask
from zatiq_aws_s3_client import ZatiqAWSS3Client
from zatiq_aws_rds_client import ZatiqAWSRDSClient
app = Flask(__name__)

@app.route('/')
def hello_world():
    return('Hello World!')

@app.route('/image/business/')
def upload_business_image_to_s3():
    zatiq_aws = ZatiqAWSS3Client()
    response = zatiq_aws.get_all_buckets()
    return(response)

@app.route('/businesses/list/')
def all_entries():
    zatiq_rds = ZatiqAWSRDSClient()
    response = zatiq_rds.get_all_businesses()
    return(response)

@app.route('/business/login/')
def business_login():
    zatiq_rds = ZatiqAWSRDSClient()
    response = zatiq_rds.business_login("test", "testing")
    if isinstance(response, str):
        return(response)
    else:
        return('' + response[0] + '\n' + response[1])

@app.route('/business/register/')
def business_register():
    zatiq_rds = ZatiqAWSRDSClient()
    response = zatiq_rds.business_register("flask", "flask@flask.com", "hasan")
    #response = zatiq_rds.business_register("test", "test", "test")
    return("hey")
