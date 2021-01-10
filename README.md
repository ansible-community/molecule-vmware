# Molecule VMware Plugin

[![](https://badge.fury.io/py/molecule-vmware.svg)](https://badge.fury.io/py/molecule-vmware) ![molecule-vmware-ci](https://github.com/sky-joker/molecule-vmware/workflows/molecule-vmware-ci/badge.svg) ![](https://img.shields.io/badge/license-MIT-brightgreen.svg)

Molecule VMware is designed to allow use of VMware vSphere environment for provisioning test resources.  
Please note that this driver is currently in its early stage of development.

# Installation and Usage

Install molecule-vmware and pre-requisites:

```
pip install molecule-vmware ansible pyvmomi
```

Please also install pywinrm if you want to use Windows in test instance.

```
pip install pywinrm
```

Create a new role with molecule using the vmware driver:

```
molecule init role <role_name> -d vmware
```

Configure `<role_name>/molecule/default/molecule.yml` with required parameters based on your vSphere environment.  
A simple config is:

```yaml
dependency:
  name: galaxy
driver:
  name: vmware
  vcenter_hostname: vcsa.local
  vcenter_username: administrator@vsphere.local
  vcenter_password: secret
  validate_certs: false
  datacenter: dc
  #esxi_hostname: change me to esxi hostname of deploying an instance. need it if not cluster specified
  cluster: cluster01
  folder: /vm/example
  vm_username: root
  vm_password: secret
  instance_os_type: linux # is possible only specify [linux or windows]
  # The below are possible parameters to be specified if using the windows template.
  #winrm_port: 5986 # is WinRM port
  #connection: winrm # is the connection type
  #winrm_transport: ntlm # is the authentication type
  #winrm_server_cert_validation: ignore # is the server certificate validation mode
platforms:
  - name: instance1
    template: CentOS7
    hardware:
      num_cpus: 2
      memory_mb: 2048
    networks:
      - name: VM Network
        type: dhcp
  - name: instance2
    template: CentOS8
    snapshot_src: linked_clone # is a snapshot name to be possible specified if you want to use linked clone.
    hardware:
      num_cpus: 2
      memory_mb: 2048
    networks:
      - name: VM Network
        ip: 100.64.0.2
        netmask: 255.255.255.0
        gateway: 100.64.0.1
    # The below are possible parameters to be specified if using the windows template.
    #customization:
    #  fullname: molecule # is the server owner name
    #  orgname: molecule # is the organization name
provisioner:
  name: ansible
verifier:
  name: ansible
```

# Template requirements

A template requires vmware tools because it is done Sysprep or Linuxprep to initialize OS.  
When Linux, please also install Perl to the template.

# License

The [MIT](https://github.com/sky-joker/molecule-vmware/blob/master/LICENSE) License.
