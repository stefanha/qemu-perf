This repository contains an Ansible playbook to run a fio disk I/O benchmark
inside a libvirt KVM guest.  It supports multiple QEMU configurations including
image files, the nvme:// userspace VFIO driver, and the null-co dummy block
driver.  Edit the files to change configuration (or check out a git commit that
corresponds to the configuration you want to benchmark).

The important files are as follows:

- files/authorized\_keys - ssh public keys for guest that you need to provide
- files/fio.job - the fio(1) benchmark configuration file
- files/test.xml - the libvirt domain XML
- benchmark.yml - the Ansible playbook
- hosts.template - the Ansible hosts file you need to customize
- analyze.py - script to print statistics from the fio JSON output files

Run the playbook like this:

    $ ansible-playbook -i hosts benchmark.yml

The fio JSON output files will be written to the local /tmp directory.
