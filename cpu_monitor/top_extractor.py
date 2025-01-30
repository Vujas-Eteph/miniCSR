# command: top -b -n 1 | awk 'NR>7 {cpu[$2]+=$9} END {for (u in cpu) print u, cpu[u]}'
# - IMPORTS -------------------------------------------------------------------
import re


# - CLASSES -------------------------------------------------------------------
class TopExtractor:
    def __init__(self):
        self._init_regex_pattern()

    def _init_regex_pattern(self):
        # Define a regex pattern to extract user and CPU usage from the 'top' output.
        # This regex assumes the format of the 'top' output, where the user is in column 2
        # and CPU usage (as a percentage) is in column 9. Adjust if needed.
        self.pattern = re.compile(
            r"^\s*(\S+)\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\d+\.\d+)\s+"
        )

    def get_cpu_usage_by_user(self, output):
        """Parses top output and aggregates CPU usage by user."""
        cpu_usage_by_user = {}

        # Split the output into lines and skip the header
        output_lines = output.splitlines()

        # Iterate through the lines of output
        for line in output_lines:
            # Split the line into key (user) and value (CPU usage)
            key, value = line.split()
            # Store the key-value pair in the dictionary, converting value to float
            cpu_usage_by_user[key] = float(value.replace(",", "."))

        return cpu_usage_by_user
