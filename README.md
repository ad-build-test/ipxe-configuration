# IPXE Configuration
This repo is used to Manage IPXE configs as a single component, generates PXE files, and centralizes the configuration

## How to make changes
1. If developer wants to modify existing cpu configuration, or add a new entry, then changes should be made at [ipxe_config.yaml](ipxe_config.yaml)
2. *Tentative* - Developer should then run [generate_ipxe_from_config.py](generate_ipxe_from_config.py), may make it run automatically whenever pushes to main are made

## Contents
1. [ipxe_config.yaml](ipxe_config.yaml) - the main configuration file, the only file developers need to edit
2. [generate_ipxe_from_config.py](generate_ipxe_from_config.py) - script to generate the .ipxe files for all the cpus in the ipxe_config.yaml, this script is called everytime ipxe_config.yaml updates
3. [post_parse_test.py](post_parse_test.py) - script to parse the generated .ipxe files and compares it to the yaml of the new current ipxe_config.yaml to ensure the files were generated properly. This is called each time the generate_ipxe_from_config.py is called. Developer can also call this manually to double check results
4. [parse_ipxe_files.py](parse_ipxe_files.py) - script to parse the existing .ipxe files and output the result into a yaml file
5. [parse_ipxe_files_extra_code.py](parse_ipxe_files_extra_code.py) - helper script for parse_ipxe_files.py
6. original_dev/facet/lcls/testfac_ipxe - these folders contain the ipxe files that exist before this repo was made
7. [ansible](ansible) - folder with the ansible playbook to deploy ipxe files, including the inventory file

## Example Usage
1. Contents of repo $`ls`
```
pnispero@PC100942:~/ipxe-configuration$ ls
README.md                              ipxe_config.yaml       parse_ipxe_files.py
__pycache__                            original_dev_ipxe      parse_ipxe_files_extra_code.py
ansible                                original_facet_ipxe    post_parse_test.py
generate_ipxe_files_from_config.py     original_lcls_ipxe     requirements.txt
generate_ipxe_files_from_config_v2.py  original_testfac_ipxe
```
2. Run generation script $`python3 generate_ipxe_files_from_config.py`
```
pnispero@PC100942:~/ipxe-configuration$ python3 generate_ipxe_files_from_config.py
Generation completed! Please see generated_<facility>_ipxe/ directories.

** PASS ** ready for deployment! The generated ipxe files match the current ipxe_config.yaml
```
3. See contents $`ls`
```
pnispero@PC100942:~/ipxe-configuration$ ls
README.md                              generated_facet_ipxe_files    original_lcls_ipxe
__pycache__                            generated_lcls_ipxe_files     original_testfac_ipxe
ansible                                generated_testfac_ipxe_files  parse_ipxe_files.py
generate_ipxe_files_from_config.py     ipxe_config.yaml              parse_ipxe_files_extra_code.py
generate_ipxe_files_from_config_v2.py  original_dev_ipxe             post_parse_test.py
generated_dev_ipxe_files               original_facet_ipxe           requirements.txt
```
4. See contents of any ipxe file $`cat generated_dev_ipxe_files/cpu-ad10-cm01.ipxe`
```
pnispero@PC100942:~/ipxe-configuration$ cat generated_dev_ipxe_files/
b221-cpu1.ipxe                cpu-b084-sp20.ipxe            cpu-b34-pm03.ipxe
cpu-ad10-cm01.ipxe            cpu-b084-test2.ipxe           cpu-b34-sp01.ipxe
cpu-as01-mg01.ipxe            cpu-b084-test3.ipxe           cpu-b34-sp02.ipxe
cpu-as01-mg02.ipxe            cpu-b084-ts01.ipxe            cpu-b34-sp03.ipxe
cpu-as01-sp01.ipxe            cpu-b130-sp01.ipxe            cpu-b34-sp04.ipxe
cpu-as01-sp02.ipxe            cpu-b131-sp01.ipxe            cpu-b34-sp05.ipxe
cpu-b033-sp01.ipxe            cpu-b15-ky01.ipxe             cpu-b34-sp06.ipxe
cpu-b084-mp01.ipxe            cpu-b15-mg01.ipxe             cpu-b34-sp07.ipxe
cpu-b084-pm01.ipxe            cpu-b15-rf01.ipxe             cpu-b34-sp08.ipxe
cpu-b084-pm02.ipxe            cpu-b15-rf03.ipxe             cpu-b34-test1.ipxe
cpu-b084-pm03.ipxe            cpu-b15-rf04.ipxe             cpu-b34-test10.ipxe
cpu-b084-pm04.ipxe            cpu-b15-sp01.ipxe             cpu-b34-test2.ipxe
cpu-b084-pm05.ipxe            cpu-b15-sp02.ipxe             cpu-b34-test3.ipxe
cpu-b084-sp01.ipxe            cpu-b15-sp03.ipxe             cpu-b34-test4.ipxe
cpu-b084-sp02.ipxe            cpu-b34-bd32.ipxe             cpu-b34-test5.ipxe
cpu-b084-sp04.ipxe            cpu-b34-bp01.ipxe             cpu-b34-test6.ipxe
cpu-b084-sp05.ipxe            cpu-b34-ck00.ipxe             cpu-b34-test7.ipxe
cpu-b084-sp06.ipxe            cpu-b34-fb01.ipxe             cpu-b34-test8.ipxe
cpu-b084-sp08.ipxe            cpu-b34-fb02.ipxe             cpu-b34-test9.ipxe
cpu-b084-sp11.ipxe            cpu-b34-mc01.ipxe             cpu-b34-ts01.ipxe
cpu-b084-sp12.ipxe            cpu-b34-mc21.ipxe             cpu-b44-sp01.ipxe
cpu-b084-sp13.ipxe            cpu-b34-mc22.ipxe             cpu-b950-sp01.ipxe
cpu-b084-sp14.ipxe            cpu-b34-mc23.ipxe             cpu-template-2016.ipxe
cpu-b084-sp15.ipxe            cpu-b34-mg01.ipxe             cpu-template-2019-32bit.ipxe
cpu-b084-sp16.ipxe            cpu-b34-mg02.ipxe             cpu-template-2019.ipxe
cpu-b084-sp17.ipxe            cpu-b34-mp01.ipxe             facet-dev01.ipxe
cpu-b084-sp18.ipxe            cpu-b34-pm01.ipxe             iocemcordev.ipxe
cpu-b084-sp19.ipxe            cpu-b34-pm02.ipxe             qemubox.ipxe
pnispero@PC100942:~/ipxe-configuration$ cat generated_dev_ipxe_files/cpu-ad10-cm01.ipxe
#!ipxe

set extra-args brd.rd_size=524288 pcie_aspm.policy=performance pci=noaer
set vers buildroot-2016.11.1-x86_64
```
5. Check ipxe_config.yaml if it does have those fields $`grep -C 3 -n 'cpu-ad10-cm01' ipxe_config.yaml`
```
pnispero@PC100942:~/ipxe-configuration$ grep -C 3 -n 'cpu-ad10-cm01' ipxe_config.yaml
75-  b221-cpu1:
76-    extra-args: brd.rd_size=524288
77-    version: buildroot-2019.08-x86_64
78:  cpu-ad10-cm01:
79-    extra-args: brd.rd_size=524288 pcie_aspm.policy=performance pci=noaer
80-    version: buildroot-2016.11.1-x86_64
81-  cpu-as01-mg01:
```
6. **Optional** Run post test again because trust issues $`python3 post_parse_test.py`
```
pnispero@PC100942:~/ipxe-configuration$ python3 post_parse_test.py

** PASS ** ready for deployment! The generated ipxe files match the current ipxe_config.yaml
```
7. **Optional** Alter a random ipxe file that was generated to see if the test is valid or just saying pass because it can $`sed -i 's/buildroot-2016.11.1-x86_64/FAKE-BUILDROOT/' generated_dev_
ipxe_files/cpu-ad10-cm01.ipxe`
```
pnispero@PC100942:~/ipxe-configuration$ sed -i 's/buildroot-2016.11.1-x86_64/FAKE-BUILDROOT/' generated_dev_
ipxe_files/cpu-ad10-cm01.ipxe
```
8. **Optional** Run post test again for trust issues $`python3 post_parse_test.py`
```
pnispero@PC100942:~/ipxe-configuration$ python3 post_parse_test.py

** FAIL ** NOT ready for deployment! The generated ipxe files DO NOT match the current ipxe_config.yaml

=== LEGEND ===
dictionary_item_added - means a field in ipxe_config.yaml exists, but not in generated ipxe file/dir

dictionary_item_removed - means a field in ipxe_config.yaml doesn't exist, but does in generated ipxe file/dir
values_changed - inconsistency between values in the ipxe_config.yaml and the corresponding generated ipxe file
================

Diff between generated ipxe files and ipxe_config.yaml:

{'values_changed': {"root['dev']['cpu-ad10-cm01']['version']": {'new_value': 'buildroot-2016.11.1-x86_64', 'old_value': 'FAKE-BUILDROOT'}}}
```
Done

