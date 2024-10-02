# IPXE Configuration
Desc: Used to Manage PXE configs as a single component, generate PXE files

## Contents
1. [ipxe_config.yaml](ipxe_config.yaml) - the main configuration file, the only file developers need to edit
2. [generate_ipxe_from_config.py](generate_ipxe_from_config.py) - script to generate the .ipxe files for all the cpus in the ipxe_config.yaml, this script is called everytime ipxe_config.yaml updates
3. [parse_original_ipxe.py](parse_original_ipxe.py) - script to parse the existing .ipxe files and output the result into a yaml file, only meant to be used to construct ipxe_config.yaml the first time.
4. [parse_original_ipxe_extra_code.py](parse_original_ipxe_extra_code.py) - helper script for parse_original_ipxe.py, only meant to be used to construct ipxe_config.yaml the first time.

## How to make changes
1. If developer wants to modify existing cpu configuration, or add a new entry, then changes should be made at [ipxe_config.yaml](ipxe_config.yaml)
