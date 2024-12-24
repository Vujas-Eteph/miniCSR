# command: ps -eo user,pcpu | awk '{cpu[$1] += $2} END {for (i in cpu) if (cpu[i] > 0) print i, cpu[i]}' | sort -k2 -nr
# - IMPORTS -------------------------------------------------------------------
import re


# - CLASSES -------------------------------------------------------------------
class CpuUsageByUserExtractor():
    def __init__(self):
        self._init_regex_pattern()

    def _init_regex_pattern(self):
        # Define a regex pattern to extract user and CPU usage
        self.pattern = re.compile(r'^(\S+)\s+(\d+\.\d+)$')

    def get_cpu_usage_by_user(self, output):
        """Parses ps output and aggregates CPU usage by user."""
        cpu_usage_by_user = {}

        # Split the output into lines and skip the header
        output_lines = output.splitlines()

        for line in output_lines[1:]:  # Skip the header line
            match = self.pattern.match(line)
            if match:
                user = match.group(1)
                try:
                    cpu_usage = float(match.group(2))
                except ValueError:
                    continue

                # Aggregate CPU usage by user
                cpu_usage_by_user[user] = cpu_usage_by_user.get(user, 0) + cpu_usage

        return cpu_usage_by_user
