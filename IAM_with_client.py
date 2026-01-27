import os
import boto3
from botocore.exceptions import ClientError

# create IAM user
def create_iam_user(username):
    try:
        iam_client = boto3.client('iam')
        response = iam_client.create_user( UserName = username )
        print(response)
        print("User created.")

    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("User already exist.")
        else:
            print("Unexpected error :", e)

# delete IAM user
def delete_user(username):
    try:
        iam_client = boto3.client('iam')
        response = iam_client.delete_user(
            UserName = username
        )    
        print(response)
        print("User deleted.")

    except ClientError as e:
        print(e)

# List Iam users
def list_users():
    iam_client = boto3.client('iam')
    response = iam_client.list_users()
    for data in response['Users']:
        print(data['UserName'])


if __name__ == "__main__":
    #create_iam_user("sam")
    #create_iam_user("john")
    list_users()
    #delete_user("john")