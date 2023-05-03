from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError


# Load the environment variables from the .env file
load_dotenv()
# create s3 instance
s3 = boto3.client('s3',
                  endpoint_url='https://s3.us-central-1.wasabisys.com',
                  aws_access_key_id=os.environ['WASABI_ACCESS_KEY'],
                  aws_secret_access_key=os.environ['WASABI_SECRET_KEY'])

# print all avilable objects in said bucket
response = s3.list_objects(Bucket='music-history-images')
print(response)

response = s3.put_object_acl(
    Bucket='music-history-images', Key='musichistorylogo.png', ACL='public-read')
print(response)

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    try:
        response = s3.generate_presigned_url('get_object',
                                             Params={
                                                 'Bucket': bucket_name, 'Key': object_name},
                                             ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None

    return response
