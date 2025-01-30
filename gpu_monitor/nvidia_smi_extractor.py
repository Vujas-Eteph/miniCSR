# - IMPORTS -------------------------------------------------------------------
import re


# - CLASSES -------------------------------------------------------------------
class NvidiaSmiPatternExtractor:
    def __init__(self):
        self._init_regex_pattern()

    def _init_regex_pattern(self):
        # Regex patterns to match important fields
        self.gpu_name_pattern = re.compile(
            r"\|\s+(\d+)\s+([A-Za-z0-9\s\-]+?)(?:\s+Off)?\s+\|"
        )
        self.fan_temp_perf_pattern = re.compile(
            r"\|\s+(N/A|\d+)%?\s+(\d+)C\s+([A-Za-z0-9]+)\s+(\d+)W\s+/\s+(\d+)W\s+\|"
        )
        self.memory_pattern = re.compile(r"\|\s+(\d+)MiB\s+/\s+(\d+)MiB\s+\|")
        self.gpu_util_pattern = re.compile(r"\|\s+(\d+)%\s+Default\s+\|")

    def _get_gpu_names(self, output):
        return self.gpu_name_pattern.findall(output)

    def _get_fan_temp(self, output):
        return self.fan_temp_perf_pattern.findall(output)

    def _get_memory_load(self, output):
        return self.memory_pattern.findall(output)

    def _get_gpu_utilization(self, output):
        return self.gpu_util_pattern.findall(output)
