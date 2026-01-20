import boto3
import json
import json_operations

config_data = json_operations.load_data("./configs/ec2_config.json")

region = config_data["region_name"]
ami_id = config_data["ami_id"]
instance_type = config_data["instance_type"]
key_name = config_data["key_name"]

def create_instance():
    ec2_client = boto3.client('ec2')
    instances = ec2_client.run_instances(
        ImageId = ami_id,
        InstanceType = instance_type,
        KeyName = key_name,
        MinCount = 1,
        MaxCount = 1
    )

    instances_id = instances["Instances"][0]["InstanceId"]
    print(instances_id)

create_instance()    