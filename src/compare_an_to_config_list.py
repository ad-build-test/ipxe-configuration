# Temporary script to compare An's curated list to the current ipxe_config.yaml
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

def get_compare_config_dict() -> dict:
    compare_config = {}
    keywords = ['set', 'vers']  # Replace with the list of known words
    second_keywords = ['set', 'extra-args']  # Replace with the list of known words
    for facility, dir_path in GENERATED_IPXE_FOLDERS.items():
        results = parse_ipxe_files.find_lines_in_directory(dir_path, keywords, second_keywords)
        compare_config[facility] = results
    return compare_config

def compare_dicts(compare_config, current_config):
    facilities = {"dev", "lcls", "facet", "testfac"}
    for facility in facilities:
        print(f"\nFaciity: {facility}\n** If empty then MATCH!!!!")
        cpus_compare_config = set(compare_config.get(facility, []))
        cpus_current_config = set(current_config.get(facility, []))
        unique_to_compare_config = cpus_compare_config - cpus_current_config
        unique_to_current_config = cpus_current_config - cpus_compare_config
        print(f"Unique cpus in current_config:\n{unique_to_current_config}")
        print(f"Unique cpus in compare_config:\n{unique_to_compare_config}")
        # for node in compare_config[facility]:
        #     print(node)
        #     if compare_config[facility][node] not in current_config[facility][node]:
            #     print(f"At facility {facility}, missing node {node} in ipxe_config.yaml")

def main():
    compare_config = parse_ipxe_files.parse_yaml_file("../An_curated_ipxe_list.yml")
    current_config = parse_ipxe_files.parse_yaml_file(IPXE_CONFIG_PATH)
    compare_dicts(compare_config, current_config)

if __name__ == '__main__':
    main()