import json
import sys

def update_params(project_name, instance_type, params_file):
    try:
        with open(params_file, 'r') as file:
            params = json.load(file)
    except Exception as e:
        print(f"Failed to load parameters file: {e}")
        sys.exit(1)

    for param in params:
        if param['ParameterKey'] == 'my-server':
            param['ParameterValue'] = project_name
        elif param['ParameterKey'] == 'InstanceType':
            param['ParameterValue'] = instance_type

    try:
        with open(params_file, 'w') as file:
            json.dump(params, file, indent=4)
    except Exception as e:
        print(f"Failed to write parameters file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python edit-template.py <project_name> <instance_type> <params_file>")
        sys.exit(1)

    project_name = sys.argv[1]
    instance_type = sys.argv[2]
    params_file = sys.argv[3]

    update_params(project_name, instance_type, params_file)
    print(f"Updated {params_file} with new parameters: project_name={project_name}, instance_type={instance_type}.")