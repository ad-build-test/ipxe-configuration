"""
Generates all the ipxe files from the ipxe_config.yaml, into seperate directories
for each facility
"""
import os
import yaml

def parse_yaml_file(file_path): 
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  # Load YAML content safely
            return data
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def generate_files_from_yaml(yaml_file_path):
    parsed_data = parse_yaml_file(yaml_file_path)

    for facility, cpus in parsed_data.items():
        # Create a directory for each facility
        facility = 'generated_' + facility + '_ipxe_files/ipxe'
        os.makedirs(facility, exist_ok=True)
        
        for cpu, fields in cpus.items():
            # Create a file for each CPU in the respective facility directory
            file_path = os.path.join(facility, f"{cpu}.ipxe")
            with open(file_path, 'w') as output_file:
                output_file.write("#!ipxe\n\n")
                for field, value in fields.items():
                    if (field == 'version'):
                        output_file.write(f"set vers {value}\n")
                    elif (field == 'extra-args'):
                        output_file.write(f"set extra-args {value}\n")
                    else:
                        print(f"Error in yaml {yaml_file_path}* incorrect field found: {field}, value: {value}, at node: {node_name}, in facility: {facility}")
            
            print(f"Generated file: {file_path}")

def main():
    generate_files_from_yaml('ipxe_config.yaml')

if __name__ == '__main__':
    main()

# TODO: only regenerate the files for cpus that changed its fields, don't want to regenerate 
        # everything each time the config file changes. 
        # 1) When this script is ran just copy the current standing ipxe_config.yaml as previous_ipxe_config.yaml
        # 2) Then compare the standing ipxe_config.yaml to previous_ipxe_config.yaml and do a delta

# import yaml
# import os

# def load_config(file_path):
#     with open(file_path, 'r') as file:
#         return yaml.safe_load(file)

# def save_generated_config(config, file_path):
#     with open(file_path, 'w') as file:
#         file.write("# Do not touch or delete this file\n")
#         yaml.dump(config, file)

# def identify_changes(current_config, generated_config):
#     changed_cpus = []
    
#     # Check for changes or new CPUs
#     for current_cpu in current_config['cpus']:
#         for generated_cpu in generated_config['cpus']:
#             if current_cpu['name'] == generated_cpu['name']:
#                 if current_cpu != generated_cpu:  # Check for changes
#                     changed_cpus.append(current_cpu)
#                 break
#         else:
#             # If not found in generated, it is new
#             changed_cpus.append(current_cpu)
    
#     return changed_cpus

# def generate_file(cpu):
#     cpu_name = cpu['name']
#     file_content = f"Version: {cpu['version']}\nOther Field: {cpu['other_field']}\n"
#     with open(f"{cpu_name}.txt", 'w') as f:
#         f.write(file_content)

# def main():
#     config_file = 'config.yaml'
#     generated_config_file = 'generated_config.yaml'

#     # Load current configuration
#     current_config = load_config(config_file)

#     # Load generated configuration if it exists
#     if os.path.exists(generated_config_file):
#         generated_config = load_config(generated_config_file)
#     else:
#         generated_config = {'cpus': []}  # If the generated config doesn't exist

#     # Identify changes
#     changed_cpus = identify_changes(current_config, generated_config)

#     # Generate files for changed CPUs
#     for cpu in changed_cpus:
#         generate_file(cpu)

#     # Save current configuration as generated config for the next run
#     save_generated_config(current_config, generated_config_file)

# if __name__ == "__main__":
#     main()
