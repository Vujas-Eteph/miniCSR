# - IMPORTS -------------------------------------------------------------------
import paramiko


# - CLASS ---------------------------------------------------------------------
class ExecuteCmdOnHostViaSSH:
    """Execude a command on ONE host"""

    def __init__(self, ssh_connection):
        self.ssh_connection = ssh_connection

    def _execute_cmd_on_host(self, command):
        """Execute cmd on the connected server"""
        try:
            stdin, stdout, stderr = (
                self.ssh_connection.ssh_client.exec_command(command)
            )
            output = stdout.read().decode()
            error = stderr.read().decode()

            stdin.close()
            stdout.close()
            stderr.close()

            if error:
                print(
                    f"Error executing command on {self.ssh_connection.hostname}:\n{error}"
                )

            return output, error

        except paramiko.SSHException as e:
            print(
                f"Failed to execute command '{command}' on {self.ssh_connection.hostname}: {str(e)}"
            )
            return None, None
