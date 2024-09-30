# Parse files
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
                            results[node_name]['extra_args'] = ' '.join(words[second_keyword_count:])
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

def parse_original_ipxe_and_output_to_yaml():
    # Find node and their buildroot versions
    directory_path = 'ipxe'  # Replace with your directory path
    keywords = ['set', 'vers']  # Replace with the list of known words
    second_keywords = ['set', 'extra-args']  # Replace with the list of known words

    node_versions_and_args_dict = find_lines_in_directory(directory_path, keywords, second_keywords)

    # Output to a YAML file
    output_file = 'node_versions_and_args_dict.yaml'  # Specify your output YAML file name
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


def parse_output_yaml_file_test():
    # Specify the YAML file to parse
    yaml_file_path = 'node_versions_and_args_dict.yaml'  # Replace with your YAML file path

    parsed_data = parse_yaml_file(yaml_file_path)

    # Print parsed data
    if parsed_data is not None:
        for filename, details in parsed_data.items():
            print(f"File: {filename}")
            for key, value in details.items():
                print(f"  {key}: {value}")
    else:
        print("No data to display.")

def main():
    parse_original_ipxe_and_output_to_yaml()

    parse_output_yaml_file_test()


if __name__ == '__main__':
    main()