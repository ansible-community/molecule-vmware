import os

from molecule.api import Driver
from molecule import logger, util

LOG = logger.get_logger(__name__)


class VMware(Driver):
    def __init__(self, config=None):
        super(VMware, self).__init__(config)
        self._name = "vmware"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def default_safe_files(self):
        return [self.instance_config]

    @property
    def default_ssh_connection_options(self):
        return self._get_ssh_connection_options()

    def login_options(self, instance_name):
        d = {"instance": instance_name}

        return util.merge_dicts(d, self._get_instance_config(instance_name))

    def ansible_connection_options(self, instance_name):
        try:
            d = self._get_instance_config(instance_name)

            if "instance_os_type" in d:
                if d['instance_os_type'] == "linux":
                    return {
                        "ansible_user": d["user"],
                        "ansible_host": d["address"],
                        "ansible_port": d["port"],
                        "ansible_private_key_file": d["identity_file"],
                        "connection": "ssh",
                        "ansible_ssh_common_args": " ".join(self.ssh_connection_options),
                    }

                if d['instance_os_type'] == "windows":
                    return {
                        "ansible_user": d["user"],
                        "ansible_host": d["address"],
                        "ansible_password": d["password"],
                        "ansible_port": d["port"],
                        "ansible_connection": d["connection"],
                        "ansible_winrm_transport": d["winrm_transport"],
                        "ansible_winrm_server_cert_validation": d["winrm_server_cert_validation"]
                    }
        except StopIteration:
            return {}
        except IOError:
            # Instance has yet to be provisioned , therefore the
            # instance_config is not on disk.
            return {}

    def _get_instance_config(self, instance_name):
        instance_config_dict = util.safe_load_file(self._config.driver.instance_config)

        return next(
            item for item in instance_config_dict if item["instance"] == instance_name
        )

    def template_dir(self):
        """Return path to its own cookiecutterm templates. It is used by init
        command in order to figure out where to load the templates from.
        """
        return os.path.join(os.path.dirname(__file__), "cookiecutter")
