import os
import json
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

# create policy
def create_policy(policyname, policy_path):

    try:
        with open(policy_path, 'r') as f:
            policydocument = json.load(f)

        policydocument = json.dumps(policydocument)    
        print(policydocument)

        iam_client = boto3.client('iam')
        response = iam_client.create_policy(
            PolicyName = policyname,
            PolicyDocument = policydocument
            
        )
        print(response)
        print('Policy created.')

    except ClientError as e:
        print(e)

# list policy
def list_policy():
    iam_client = boto3.client('iam')
    response = iam_client.list_policies(
        Scope = 'Local'
    )
    for policy in response['Policies']:
        print(policy['PolicyName'])

#fetch arn of policy
def get_arn(policyname):
    iam_client = boto3.client('iam')
    response = iam_client.list_policies( Scope = 'Local' )
    for policy in response['Policies']:
        if policy['PolicyName'] == policyname:
            return policy['Arn']
    return False

# delete policy
def delete_policy(policyname):
    policyarn = get_arn(policyname)
    print(policyarn)

    if policyarn:
        iam_client = boto3.client('iam')
        response = iam_client.delete_policy(
            PolicyArn = policyarn
        )
        print(response)
    else:
        print("Policy not found")


if __name__ == "__main__":
    #create_iam_user("sam")
    #create_iam_user("john")
    list_users()
    delete_user("sam")
    #create_policy("sam_ec2_full_access", "./data/ec2_access_policy.json")
    #delete_policy("sam_ec2_full_access")