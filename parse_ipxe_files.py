""" 
Desc: 
    This script parses ipxe files and puts it into a yaml file. Non-destructive,
    does not alter existing ipxe files

Usage:
    python3 parse_ipxe_files.py <dir>
"""
import argparse
import os
import yaml  

def find_lines_in_directory(directory_path, keywords, second_keywords):
    results = {}
    keyword_count = len(keywords)
    second_keyword_count = len(second_keywords)

    # Loop through each file in the directory
    for filename in sorted(os.listdir(directory_path)):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it is a file
        if os.path.isfile(file_path):
            found_lines = False  # Track if any lines were found
            node_name, file_ext = os.path.splitext(filename) # Slice out the file extension from node name ex: cpu-b34-bp01.ipxe
            if (file_ext.lower() != '.ipxe'): # Skip non .ipxe files
                continue
            try:
                results[node_name] = {
                    'version': '',
                    'extra-args': '',
                    'additional': ''
                }  # Initialize the dictionary for each file
                with open(file_path, 'r') as file:
                    for line in file:
                        stripped_line = line.strip()
                        words = stripped_line.split()

                        # Skip comments and newlines
                        if stripped_line.startswith('#') or not stripped_line:
                            continue    
                        
                        # Check for the first keywords
                        elif len(words) >= keyword_count and words[:keyword_count] == keywords:
                            results[node_name]['version'] = ' '.join(words[keyword_count:])
                            found_lines = True
                        
                        # Check for the second keywords
                        elif len(words) >= second_keyword_count and words[:second_keyword_count] == second_keywords:
                            results[node_name]['extra-args'] = ' '.join(words[second_keyword_count:])
                            found_lines = True

                        # if there are other lines that aren't comments, add them to 'additional' field
                        else:
                            results[node_name]['additional'] += line
                    
            except Exception as e:
                print(f"Could not read {filename}: {e}")

            # Check if neither line was found
            if not found_lines:
                print(f"Warning: {filename} did not match any specified lines.")
                results.pop(node_name)  # Remove empty entry
                continue

            # Remove empty entries
            if (results[node_name]["extra-args"] == ''):
                results[node_name].pop('extra-args')
            if (results[node_name]["additional"] == ''):
                results[node_name].pop('additional')

    return results

# custom representer for long strings, used to imporve format for strings with \n
def str_presenter(dumper, data):
    """configures yaml for dumping multiline strings
    Ref: https://stackoverflow.com/questions/8640959/how-can-i-control-what-scalar-form-pyyaml-uses-for-my-data"""
    if len(data.splitlines()) > 1:  # check for multiline string
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

def parse_ipxe_files_and_output_to_yaml(dir_path: str):
    # Find node and their buildroot versions
    keywords = ['set', 'vers']  # Replace with the list of known words
    second_keywords = ['set', 'extra-args']  # Replace with the list of known words

    nodes_config_dict = find_lines_in_directory(dir_path, keywords, second_keywords)

    # Output to a YAML file
    output_file = dir_path + '/node_versions_and_args.yaml'  # Specify your output YAML file name
    with open(output_file, 'w') as yaml_file:
        yaml_file.write("## Generated file from parse_ipxe_files.py - meant to be inspected then copied over to main ipxe-config.yaml at TOP of repo ##\n")
        
        # to format string with newlines
        yaml.add_representer(str, str_presenter)
        yaml.representer.SafeRepresenter.add_representer(str, str_presenter) # to use with safe_dum
        yaml.dump(nodes_config_dict, yaml_file, default_flow_style=False, sort_keys=False)

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


def main():
    # TODO: Edit parser to look for code that are non-comments, but also not the vers or extra-args
    # and put them into an 'additional' field that can be multiline. 
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", help="directory path to ipxe files to parse",
                        type=str)
    args = parser.parse_args()
    dir_path = args.dir_path
    if (dir_path.endswith('/')): # Remove the '/'
        dir_path = dir_path[:-1]

    parse_ipxe_files_and_output_to_yaml(dir_path)

    # parse_output_yaml_file_test(dir_path)

if __name__ == '__main__':
    main()