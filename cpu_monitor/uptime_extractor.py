# - IMPORTS -------------------------------------------------------------------
import re


# - CLASSES -------------------------------------------------------------------
class UptimePatternExtractor():
    def __init__(self):
        self._init_regex_pattern()

    def _init_regex_pattern(self):
        # Regex pattern to match uptime output, allowing both dot and comma as decimal separators
        self.uptime_pattern = re.compile(
            r"up\s+([\d\s\w,:]+),\s+(\d+)\s+users?,\s+load\s+average:\s+([\d,]+),\s+([\d,]+),\s+([\d,]+)"
        )

    def get_uptime_info(self, output):
        match = self.uptime_pattern.search(output)
        if match:
            uptime = match.group(1)  # Uptime (e.g., "10 days, 3:45")
            # users = int(match.group(2))  # Number of users (e.g., 4)
            load_1min = float(match.group(3).replace(',', '.'))
            load_5min = float(match.group(4).replace(',', '.'))
            load_15min = float(match.group(5).replace(',', '.'))
        else:
            raise ValueError("Could not parse uptime output.")

        return {
            "uptime": uptime,
            "load_1min": load_1min,
            "load_5min": load_5min,
            "load_15min": load_15min
        }
