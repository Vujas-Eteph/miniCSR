# - IMPORTS -------------------------------------------------------------------
from .cmd_to_host import ExecuteCmdOnHostViaSSH


# - CLASS ---------------------------------------------------------------------
class ManageCmdsToHosts:
    """Manage the commands to be run on MULTIPLE hosts"""
    def __init__(self, ssh_connection_manager):
        """
        Initialize with an SSHHostManager instance.
        This class is the in-between that allows selecting a server and executing commands.
        """
        self.ssh_connection_manager = ssh_connection_manager

    def execute_cmd_on_host(self, server_alias, cmd):
        connection = self.ssh_connection_manager.get_connection(server_alias)
        if connection:
            executor = ExecuteCmdOnHostViaSSH(connection)
            output, error = executor._execute_cmd_on_host(cmd)

            return output, error
        else:
            print(f"Cannot execute command. No active connection for {server_alias}.")

            return None, None
