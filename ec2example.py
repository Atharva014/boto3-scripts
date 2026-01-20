import boto3
import json
import json_operations

config_data = json_operations.load_data("./configs/ec2_config.json")

region = config_data["region_name"]
ami_id = config_data["ami_id"]
instance_type = config_data["instance_type"]
key_name = config_data["key_name"]
ec2_data_path = config_data["ec2_data_path"]
ec2_data = json_operations.load_data(ec2_data_path)

ec2_client = boto3.client('ec2', region_name = region)

def create_instance():
    instances = ec2_client.run_instances(
        ImageId = ami_id,
        InstanceType = instance_type,
        KeyName = key_name,
        MinCount = 1,
        MaxCount = 1
    )

    instance_id = instances["Instances"][0]["InstanceId"]
    print(instance_id)

    if "ec2_instance_ids" in ec2_data:
        ec2_data["ec2_instance_ids"].append(instance_id)
    else:
         ec2_data["ec2_instance_ids"] = [instance_id]

def read_instance_ip():
    reservations = ec2_client.describe_instances(InstanceIds = [""]).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))


if __name__ == "__main__":
    create_instance()

    if json_operations.save_json_data(ec2_data_path, ec2_data):
        print("File updated")