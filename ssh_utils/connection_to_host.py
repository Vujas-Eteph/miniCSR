# - IMPORTS -------------------------------------------------------------------
import os
import paramiko
import socket


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

    def check_connection(self, timeout=5):
        """Check if the server is reachable before trying SSH"""
        try:
            with socket.create_connection((self.hostname, self.port), timeout):
                print(f"Server {self.hostname} is reachable")
                return True
        except (socket.timeout, ConnectionRefusedError) as e:
            print(f"Cannot reach {self.hostname}")
            return False
        except Exception as e:
            print(f"Unexpected error checking {self.hostname}: {e}")
            return False

    def connect(self, password):
        """Establish ssh connection with password"""
        try:
            self.ssh_client.connect(hostname=self.hostname, port=self.port,
                                    username=self.username, password=password)
        except paramiko.SSHException as e:
            print(f"Failed to connect to {self.alias}: {str(e)}.")

    def close(self):
        """Close the SSH connection"""
        self.ssh_client.close()
        print(f"SSH connection to {self.alias} closed.")
