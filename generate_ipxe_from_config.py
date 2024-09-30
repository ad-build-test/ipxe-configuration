# Parse files
import argparse
import os
import yaml  # Ensure you have PyYAML installed: pip install pyyaml

def find_lines_in_directory(directory_path, keywords, second_keywords):
    results = {}
    keyword_count = len(keywords)
    second_keyword_count = len(second_keywords)

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it is a file
        if os.path.isfile(file_path):
            found_lines = False  # Track if any lines were found
            node_name, _ = os.path.splitext(filename) # Slice out the file extension from node name ex: cpu-b34-bp01.ipxe
            try:
                results[node_name] = {}  # Initialize the dictionary for each file
                with open(file_path, 'r') as file:
                    for line in file:
                        words = line.strip().split()
                        
                        # Check for the first keywords
                        if len(words) >= keyword_count and words[:keyword_count] == keywords:
                            results[node_name]['version'] = ' '.join(words[keyword_count:])
                            found_lines = True
                        
                        # Check for the second keywords
                        elif len(words) >= second_keyword_count and words[:second_keyword_count] == second_keywords:
                            results[node_name]['extra-args'] = ' '.join(words[second_keyword_count:])
                            found_lines = True
                        
                        # Break if both lines are found
                        if len(results[node_name]) == 2:
                            break
            
            except Exception as e:
                print(f"Could not read {filename}: {e}")

            # Check if neither line was found
            if not found_lines:
                print(f"Warning: {filename} did not match any specified lines.")
                results.pop(node_name)  # Remove empty entry

    return results

def parse_original_ipxe_and_output_to_yaml(dir_path: str):
    # Find node and their buildroot versions
    keywords = ['set', 'vers']  # Replace with the list of known words
    second_keywords = ['set', 'extra-args']  # Replace with the list of known words

    node_versions_and_args_dict = find_lines_in_directory(dir_path, keywords, second_keywords)

    # Output to a YAML file
    output_file = dir_path + '/node_versions_and_args.yaml'  # Specify your output YAML file name
    with open(output_file, 'w') as yaml_file:
        yaml.dump(node_versions_and_args_dict, yaml_file)

    print(f"Results have been written to {output_file}.")

def parse_yaml_file(file_path): 
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)  # Load YAML content safely
            return data
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def parse_output_yaml_file_test(dir_path: str):
    # Specify the YAML file to parse
    yaml_file_path = dir_path + '/node_versions_and_args.yaml'  # Replace with your YAML file path

    parsed_data = parse_yaml_file(yaml_file_path)

    # Print parsed data
    if parsed_data is not None:
        for filename, details in parsed_data.items():
            print(f"File: {filename}")
            for key, value in details.items():
                print(f"  {key}: {value}")
    else:
        print("No data to display.")

def generate_files_from_yaml(yaml_file_path, output_directory):
    parsed_data = parse_yaml_file(yaml_file_path)

    # Ensure output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Iterate over each entry in the YAML data
    for node_name, details in parsed_data.items():
        file_name = f"{node_name}.ipxe"  # Create a file name based on the entry
        file_path = os.path.join(output_directory, file_name)

        # Write the specified lines into the file
        with open(file_path, 'w') as output_file:
            output_file.write("#!ipxe\n")
            for key, value in details.items():
                if (key == 'version'):
                    output_file.write(f"set vers {value}\n")
                elif (key == 'extra-args'):
                    output_file.write(f"set extra-args {value}\n")
                else:
                    print(f"Error in yaml {yaml_file_path}* incorrect key found: {key}, value: {value}, at node: {node_name}")

        print(f"Generated file: {file_path}")

def main():
    # TODO: Won't need argparse once the configuration file has been made, since it'll be at the $TOP of dir
    parser = argparse.ArgumentParser()
    parser.add_argument("yaml_file", help="path to configuration yaml file",
                        type=str)
    args = parser.parse_args()

    # TODO: Run this multiple times, or split into different directories, can do logic
    # with every new facility create a folder 'generated_<facility>_ipxe'
    generate_files_from_yaml(args.dir_path + 'node_versions_and_args.yaml', 'generated_dev_ipxe')


if __name__ == '__main__':
    main()