""" 
Desc: 
    Similar to the parse_ipxe_files.py except this one checks
    for other lines that aren't comments, and aren't set vers or extra-args
    prints them out. Non-destructive

Usage: 
    python3 parse_ipxe_files_extra_code.py
"""
# Parse files
import argparse
import os

def find_lines_in_directory(directory_path, keywords, second_keywords):
    results = {}
    keyword_count = len(keywords)
    second_keyword_count = len(second_keywords)

    # Loop through each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        # Skip .yaml file (generated)
        if (filename.endswith('.yaml')):
            continue
        
        # Check if it is a file
        if os.path.isfile(file_path):
            found_lines = False  # Track if any lines were found
            node_name, _ = os.path.splitext(filename) # Slice out the file extension from node name ex: cpu-b34-bp01.ipxe
            try:
                results[node_name] = {}  # Initialize the dictionary for each file
                with open(file_path, 'r') as file:
                    for line in file:

                        # Skip comments
                        stripped_line = line.strip()
                        if stripped_line.startswith('#') or not stripped_line:
                            continue    

                        words = line.strip().split()
                        
                        # Check for the first keywords
                        if len(words) >= keyword_count and words[:keyword_count] == keywords:
                            results[node_name]['version'] = ' '.join(words[keyword_count:])
                            found_lines = True
                        
                        # Check for the second keywords
                        elif len(words) >= second_keyword_count and words[:second_keyword_count] == second_keywords:
                            results[node_name]['extra_args'] = ' '.join(words[second_keyword_count:])
                            found_lines = True

                        # if there are other lines that aren't comments, notify user
                        else:
                            print(f"** Found non-comment line that isn't set vers or extra-args in file: {filename} **")
                            print(stripped_line)
                        
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

def parse_ipxe_files(dir_path: str):
    # Find node and their buildroot versions
    keywords = ['set', 'vers']  # Replace with the list of known words
    second_keywords = ['set', 'extra-args']  # Replace with the list of known words

    node_versions_and_args_dict = find_lines_in_directory(dir_path, keywords, second_keywords)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir_path", help="directory path to ipxe files to parse",
                        type=str)
    args = parser.parse_args()
    parse_ipxe_files(args.dir_path)


if __name__ == '__main__':
    main()