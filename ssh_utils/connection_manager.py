# - IMPORTS -------------------------------------------------------------------
import getpass

from .config_parser import SSHConfigParser
from .connection_to_host import ConnectionToHostViaSSH


# - CLASS ---------------------------------------------------------------------
class ConnectionManagerViaSSH:
    def __init__(self, arg_password):
        """Initialize the manager for handling MULTIPLE ssh connections"""
        self.ssh_config = SSHConfigParser()
        self.connections = {}
        self.password = arg_password

    def add_connection(self, server_alias):
        """Add server connection"""
        if server_alias not in self.connections:
            connection = ConnectionToHostViaSSH(server_alias, self.ssh_config)
            if connection.check_connection():
                self.connections[server_alias] = connection
        else:
            print(f"Connection for {server_alias} already exists.")

    def connect_to_server(self, server_alias):
        """Prompt for password and connect to the specified server"""
        if server_alias in self.connections:
            if not self.password:
                self.password = getpass.getpass("password: ")
            self.connections[server_alias].connect(self.password)
        else:
            print(f"No connection found for {server_alias}.")

    def check_current_servers_alive(self):
        """Return the server alias which have a valid ssh connection"""
        return list(self.connections.keys())

    def get_connection(self, server_alias):
        """Get the SSH connection for a specific server"""
        if server_alias in self.connections:
            return self.connections[server_alias]
        else:
            print(f"No connection found for {server_alias}.")
            return None

    def close_connection(self, server_alias):
        """Close connection for specific server"""
        if server_alias in self.connections:
            self.connections[server_alias].close()
            del self.connections[server_alias]
        else:
            print(f"No connection found for {server_alias}.")

    def close_all_connections(self):
        for server_alias in list(self.connections.keys()):
            self.close_connection(server_alias)
