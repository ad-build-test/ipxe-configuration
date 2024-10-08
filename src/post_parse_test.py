""" 
Desc: 
    This script parses the generated .ipxe files and compares it to the yaml of the new
    current ipxe_config.yaml to ensure the files were generated properly.
    This is called each time the generate_ipxe_files_from_config.py is called.
    Developer can also call this manually to double check results

Usage: 
    python3 post_parse_test.py

"""
import parse_ipxe_files
from deepdiff import DeepDiff

IPXE_CONFIG_PATH="../ipxe_config.yaml"
GENERATED_IPXE_FOLDERS = {
    "dev": "../build_results/generated_dev_ipxe_files",
    "facet": "../build_results/generated_facet_ipxe_files",
    "lcls": "../build_results/generated_lcls_ipxe_files",
    "testfac": "../build_results/generated_testfac_ipxe_files"
}

def get_generated_config_dict() -> dict:
    generated_config = {}
    keywords = ['set', 'vers']  # Replace with the list of known words
    second_keywords = ['set', 'extra-args']  # Replace with the list of known words
    for facility, dir_path in GENERATED_IPXE_FOLDERS.items():
        results = parse_ipxe_files.find_lines_in_directory(dir_path, keywords, second_keywords)
        generated_config[facility] = results
    return generated_config

def compare_dicts(generated_config, current_config):
    if (generated_config == current_config):
        print("\n** PASS ** ready for deployment! The generated ipxe files match the current ipxe_config.yaml")
    else:
        print("\n** FAIL ** NOT ready for deployment! The generated ipxe files DO NOT match the current ipxe_config.yaml")
        diff = DeepDiff(generated_config, current_config)
        print("\n=== LEGEND === \
              \ndictionary_item_added - means a field in ipxe_config.yaml exists, but not in generated ipxe file/dir\
              \ndictionary_item_removed - means a field in ipxe_config.yaml doesn't exist, but does in generated ipxe file/dir\
              \nvalues_changed - inconsistency between values in the ipxe_config.yaml and the corresponding generated ipxe file\
              \n================")
        print("\nDiff between generated ipxe files and ipxe_config.yaml:\n")
        print(diff)

def main():
    # use the parse_ipxe_files script to parse the generated folders, create a config yaml, 
        # Then compare that yaml to the actual config.yaml to ensure they're a match
    generated_config = get_generated_config_dict()
    current_config = parse_ipxe_files.parse_yaml_file(IPXE_CONFIG_PATH)
    compare_dicts(generated_config, current_config)

if __name__ == '__main__':
    main()