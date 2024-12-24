# - IMPORTS -------------------------------------------------------------------
from pathlib import Path


# - CLASSES -------------------------------------------------------------------
class SSHConfigParser:
    def __init__(self, file_path=None):
        self.config = {}
        if file_path is None:
            file_path = str(Path.home() / ".ssh" / "config")
        self._read_ssh_config_file(file_path)

    def _read_ssh_config_file(self, file_path):
        file_path = Path(file_path)  # Ensure Path object
        if not file_path.exists():
            raise FileNotFoundError(f"SSH config file not found: {file_path}, "
                                    "expected it in <usermame>/.ssh/config")

        current_host = None
        try:
            with open(file_path, 'r') as file:
                current_host = None
                for line in file:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue  # Skip empty lines and comments
                    if line.startswith('Host '):
                        current_host = line.split()[1]
                        self.config[current_host] = {}
                    elif current_host and line:
                        key_value = line.split(None, 1)
                        # Ensure there is a key and value
                        if len(key_value) == 2:
                            key, value = key_value
                            self.config[current_host][key] = value
        except Exception as e:
            raise RuntimeError(f"Error parsing SSH config file: {e}")

    def get_host_config(self, host_alias):
        host_config = self.config.get(host_alias, {})
        return (
            host_config.get('HostName'),
            host_config.get('User'),
            host_config.get('Port'),
            host_config.get('IdentityFile'),  # id_rsa
            host_config.get('UserKnownHostsFile')  # known_host
        )


# Main Loop # Test
if __name__ == "__main__":
    # Usage example:
    ssh_config = SSHConfigParser()
    GPU_server_alias = '8erver'
    print(ssh_config.get_host_config(GPU_server_alias))
