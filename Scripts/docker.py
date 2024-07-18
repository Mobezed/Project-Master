from ruamel.yaml import YAML
import sys

def update_userdata(enable_docker, cloudformation_file):
    yaml = YAML()
    yaml.preserve_quotes = True

    try:
        with open(cloudformation_file, 'r') as file:
            cloudformation = yaml.load(file)
    except Exception as e:
        print(f"Failed to load YAML file: {e}")
        sys.exit(1)

    if cloudformation is None:
        print("Failed to parse YAML file.")
        sys.exit(1)

    userdata_docker = [
        "\n",
        [
            '#!/bin/bash',
            'sudo yum update -y',
            'sudo yum upgrade -y',
            'sudo amazon-linux-extras install docker -y',
            'sudo service docker start',
            'sudo usermod -a -G docker ec2-user',
            'sudo chkconfig docker on',
            'docker run  -p 21:21 -d rg.fr-par.scw.cloud/pa-ns/docker-anon-ftp:latest',
        ]
    ]

    userdata_no_docker = [
        "\n",
        [
            '#!/bin/bash',
            'sudo yum update -y',
            'sudo yum upgrade -y'
        ]
    ]

    new_userdata = userdata_docker if enable_docker else userdata_no_docker

    if 'Resources' in cloudformation:
        if 'myInstance0' in cloudformation['Resources']:
            cloudformation['Resources']['myInstance0']['Properties']['UserData'] = {"Fn::Base64": {"Fn::Join": new_userdata}}
        if 'myInstance1' in cloudformation['Resources']:
            cloudformation['Resources']['myInstance1']['Properties']['UserData'] = {"Fn::Base64": {"Fn::Join": new_userdata}}

    try:
        with open(cloudformation_file, 'w') as file:
            yaml.Representer.ignore_aliases = lambda self, data: True
            yaml.dump(cloudformation, file)
    except Exception as e:
        print(f"Failed to write YAML file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python docker.py <true|false> <cloudformation_file>")
        sys.exit(1)

    enable_docker = sys.argv[1].lower() == 'true'
    cloudformation_file = sys.argv[2]

    update_userdata(enable_docker, cloudformation_file)
    print(f"Updated {cloudformation_file} with new UserData configuration.")