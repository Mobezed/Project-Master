from ruamel.yaml import YAML
import sys

def transform_to_yaml(input_text):
    rules = []
    lines = input_text.strip().split("\n")
    for line in lines:
        cidr, port = line.split(',')
        rule = {
            "ToPort": port,
            "FromPort": port,
            "CidrIp": cidr,
            "IpProtocol": "tcp"
        }
        rules.append(rule)
    
    return rules

def update_cloudformation(input_text, cloudformation_file):
    yaml = YAML()
    with open(cloudformation_file, 'r') as file:
        cloudformation = yaml.load(file)

    new_rules = transform_to_yaml(input_text)
    
    cloudformation['Resources']['InstanceSecurityGroup']['Properties']['SecurityGroupIngress'] = new_rules

    with open(cloudformation_file, 'w') as file:
        yaml.dump(cloudformation, file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python open-flow.py '<input_text>' <cloudformation_file>")
        sys.exit(1)
    
    input_text = sys.argv[1]
    cloudformation_file = sys.argv[2]
    
    update_cloudformation(input_text, cloudformation_file)
    print(f"Updated {cloudformation_file} with new security group rules.")