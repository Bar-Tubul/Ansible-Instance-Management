import boto3
import json

region = 'us-east-1'

# Initialize a session using Amazon EC2
ec2 = boto3.client('ec2', region_name=region)

def get_instance_tags():
    response = ec2.describe_instances()
    instances = [i for r in response['Reservations'] for i in r['Instances']]

    tags = {}
    for instance in instances:
        instance_id = instance['InstanceId']
        instance_name = 'Unknown'
        for tag in instance.get('Tags', []):
            if tag['Key'] == 'Name':
                instance_name = tag['Value']
                break

        tag_dict = {tag['Key']: tag['Value'] for tag in instance.get('Tags', [])}
        tags[instance_name] = tag_dict

    return tags

def save_tags_to_file(tags, file_path):
    with open(file_path, 'w') as file:
        json.dump(tags, file, indent=4)

if __name__ == "__main__":
    tags = get_instance_tags()
    save_tags_to_file(tags, '/etc/ansible/instance_tags.json')

