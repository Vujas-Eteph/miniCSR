# - IMPORTS -------------------------------------------------------------------
import os
import paramiko


# - CLASS ---------------------------------------------------------------------
class ConnectionToHostViaSSH:
    def __init__(self, server_alias, ssh_config):
        "Init. ssh connection with ONE server"
        self.alias = server_alias
        self.hostname, self.username, self.port, self.id_rsa_key, \
            self.known_hosts = ssh_config.get_host_config(self.alias)
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.ssh_client.load_host_keys(os.path.expanduser(self.known_hosts))

    def connect(self, password):
        """Establish ssh connection with password"""
        try:
            self.ssh_client.connect(hostname=self.hostname, port=self.port,
                                    username=self.username, password=password)
            print(f"Connected to {self.alias}")
        except paramiko.SSHException as e:
            print(f"Failed to connect to {self.alias}: {str(e)}.")

    def close(self):
        """Close the SSH connection"""
        self.ssh_client.close()
        print(f"SSH connection to {self.alias} closed.")
