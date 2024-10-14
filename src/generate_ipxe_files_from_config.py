"""
Desc:
    Generates all the ipxe files from the ipxe_config.yaml, into seperate directories
    for each facility. Non-destructive, does not alter the ipxe_config.yaml

Usage:
    python3 generate_ipxe_files_from_config.py
"""
import os
import shutil
import yaml
import post_parse_test


IPXE_CONFIG_PATH="../ipxe_config.yaml"

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
    build_results = '../build_results'
    # Delete existing build results
    if os.path.exists(build_results) and os.path.isdir(build_results):
        shutil.rmtree(build_results)

    for facility, cpus in parsed_data.items():
        # Create a directory for each facility
        facility = '../build_results/generated_' + facility + '_ipxe_files'
        os.makedirs(facility, exist_ok=True)
        
        for cpu, fields in cpus.items():
            # Create a file for each CPU in the respective facility directory
            file_path = os.path.join(facility, f"{cpu}.ipxe")
            with open(file_path, 'w') as output_file:
                output_file.write("#!ipxe\n\n")
                for field, value in fields.items():
                    if (field.lower() == 'version'):
                        output_file.write(f"set vers {value}\n")
                    elif (field.lower() == 'extra-args'):
                        output_file.write(f"set extra-args {value}\n")
                    elif (field.lower() == 'additional'):
                        output_file.write(f"{value}\n")
                    else:
                        print(f"Error in yaml {yaml_file_path}* incorrect field found: {field}, value: {value}, at cpu: {cpu}, in facility: {facility}")
            
            # print(f"Generated file: {file_path}")

def main():
    generate_files_from_yaml(IPXE_CONFIG_PATH)
    print("Generation completed! Please see generated_<facility>_ipxe/ directories.")
    post_parse_test.main() # Run test to make sure configuration was done correctly

if __name__ == '__main__':
    main()