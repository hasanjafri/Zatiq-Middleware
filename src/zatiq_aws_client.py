import boto3, botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET

class ZatiqAWSClient(object):
    def __init__(self):
        self.s3_client = boto3.client("s3", aws_access_key_id=S3_KEY, aws_secret_access_key=S3_SECRET)
        self.download_s3 = boto3.resource('s3')

    def create_new_s3_bucket(self):
        self.s3_client.create_bucket(Bucket="zatiq-user-images")

    def get_all_buckets(self):
        response = self.s3_client.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        print("Bucket List: %s" % buckets)
    
    def upload_file_to_s3(self):
        self.s3_client.upload_file('./sample.jpg', 'zatiq-user-images', 'sample.jpg')
    
    def download_file_from_s3(self):
        try:
            self.download_s3.Bucket('zatiq-user-images').download_file('sample.jpg', './downloadedfroms3.jpg')
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The file does not exist in the s3 bucket!")
            else:
                raise


#download_s3.meta.client.download_file("zatiq-user-images", "test.txt", "./downloadedfroms3.txt")
