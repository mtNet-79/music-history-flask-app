from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import ClientError









# Load the environment variables from the .env file
load_dotenv()
# create s3 instance
s3 = boto3.client('s3',
                  endpoint_url='https://s3.us-west-2.amazonaws.com',
                  aws_access_key_id=os.environ['AWS_ACCESS_KEY'],
                  aws_secret_access_key=os.environ['AWS_SECRET_KEY'])

# print all avilable objects in said bucket
# response = s3.list_objects(Bucket='mt-music-history')
# print(f'my s3 response: {response}')


# response = s3.put_object_acl(
#     Bucket='mt-music-history', Key='MusicHistoryLogo.jpeg', ACL='public-read')


def generate_presigned_url(bucket_name, object_name, operation='get_object', expiration=3600):
    try:
        response = s3.generate_presigned_url(operation,
                                             Params={
                                                 'Bucket': bucket_name, 'Key': object_name},
                                             ExpiresIn=expiration)
    except ClientError as e:
        print(e)
        return None

    return response


