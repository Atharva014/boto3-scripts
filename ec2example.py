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

# create insatcne function
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

    if json_operations.save_json_data(ec2_data_path, ec2_data):
        print("File updated")

# delete single instance function
def delete_single_instance(instance_id):
    response = ec2_client.terminate_instances( InstanceIds = [ instance_id ] )
    print(response)
    ec2_data["ec2_instance_ids"].remove(instance_id)

    if json_operations.save_json_data(ec2_data_path, ec2_data):
        print("File updated")

# delete instances function
def delete_instance(instance_ids):
    response = ec2_client.terminate_instances( InstanceIds = instance_ids )
    print(response)
    final_instance_list = list(filter( lambda x: (x not in instance_ids), ec2_data["ec2_instance_ids"] ) )
    ec2_data["ec2_instance_ids"] = final_instance_list

    if json_operations.save_json_data(ec2_data_path, ec2_data):
        print("File updated")

# read public ip of instances
def read_instance_ip():
    instances_ids = ec2_data.get("ec2_instance_ids", [])
    if not instances_ids:
        print("No instance IDs found in data file")
        return

    reservations = ec2_client.describe_instances(InstanceIds = instances_ids).get("Reservations")

    for reservation in reservations:
        for instance in reservation['Instances']:
            print(instance.get("PublicIpAddress"))

# start instance
def start_instance(instance_id):
    response = ec2_client.start_instances( InstanceIds=[ instance_id ] )
    print(response)

# stop instance
def stop_instance(instance_id):
    response = ec2_client.stop_instances( InstanceIds = [ instance_id ] )
    print(response)

if __name__ == "__main__":
    create_instance()
    #print("Instance started")
    
    #read_instance_ip()

    #delete_instance(ec2_data["ec2_instance_ids"])
    
    #stop_instance(ec2_data["ec2_instance_ids"][0])
    #print("Instance stopped")

    #start_instance(ec2_data["ec2_instance_ids"][0])
    #print("Instance started")
    