import os
import boto3
from botocore.exceptions import ClientError
import logging

# create bucket
def create_bucket(bucket_name, region=None):
    try:
        if region is None:
            region = "ap-south-1"

        s3_client = boto3.client('s3', region_name = region)
        response = s3_client.create_bucket(
            Bucket = bucket_name,
            CreateBucketConfiguration ={
                'LocationConstraint': region
            }
        )
        print("Bucket created.")

    except ClientError as e:
        logging.error(e)
        return False
    
# list buckets
def list_buckets(region=None):
    try:
        if region is None:
            region = "ap-south-1"

        s3_client = boto3.client('s3', region_name = region)
        response = s3_client.list_buckets(
            BucketRegion = region
        )
        print(response)
        for bucket in response["Buckets"]:
            print(bucket["Name"])

    except ClientError as e:
        logging.error(e)
        return False

# upload file in bucket
def upload_file(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        s3_client = boto3.client('s3')
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e :
        logging.error(e)
        return False
    
    print("file uploaded")
    return True

# delete empty bucket
def delete_empty_bucket(bucket_name, region=None):
    if region is None:
        region = "ap-south-1"
    s3_client = boto3.client('s3', region_name = region)
    response = s3_client.delete_bucket(Bucket = bucket_name)
    print(response)
    print("Bucket deleted.")

# delete non-empty bucket
def delete_non_empty_bucket(bucket):
    s3_resource = s3 = boto3.resource('s3') 
    bucket_resource = s3_resource.Bucket(bucket)
    bucket_resource.objects.all().delete()
    bucket_resource.meta.client.delete_bucket(Bucket=bucket)


if __name__ == "__main__":
    bucket_name = "atharva56787685"
    region = "ap-south-1"

    #create_bucket(bucket_name, region)

    #list_buckets(region)

    #pload_file("./data/ec2data.json", bucket_name)

    #delete_empty_bucket(bucket_name, region)

    #delete_non_empty_bucket(bucket_name)