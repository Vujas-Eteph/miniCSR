# - IMPORTS -------------------------------------------------------------------
import re


# - CLASSES -------------------------------------------------------------------
class FreePatternExtractor():
    def __init__(self):
        self._init_regex_pattern()

    def _init_regex_pattern(self):
        # Regex patterns to match important fields from the `free` command output
        self.memory_pattern = \
            re.compile(r"Mem:\s+(\d+)\s+(\d+)\s+(\d+)\s+\d+\s+(\d+)\s+\d+")
        self.swap_pattern = \
            re.compile(r"Swap:\s+(\d+)\s+(\d+)\s+(\d+)")

    def _get_mem_info(self, output):
        memory_match = self.memory_pattern.search(output)
        if memory_match:
            total_memory = int(memory_match.group(1))  # Total memory in MiB
            used_memory = int(memory_match.group(2))   # Used memory in MiB
            free_memory = int(memory_match.group(3))   # Free memory in MiB
            buffer_cache = int(memory_match.group(4))  # Buffer/cache memory in MiB
        else:
            raise ValueError("Could not find memory information in free output.")
        return total_memory, used_memory, free_memory, buffer_cache

    def _get_swap_info(self, output):
        swap_match = self.swap_pattern.search(output)
        if swap_match:
            total_swap = int(swap_match.group(1))      # Total swap in MiB
            used_swap = int(swap_match.group(2))       # Used swap in MiB
            free_swap = int(swap_match.group(3))       # Free swap in MiB
        else:
            total_swap = used_swap = free_swap = 0
        return total_swap, used_swap, free_swap

    def get_free_info(self, free_output):
        """Extract memory information from the free command output."""
        total_memory, used_memory, free_memory, buffer_cache = \
            self._get_mem_info(free_output)
        total_swap, used_swap, free_swap = \
            self._get_swap_info(free_output)

        return {
            "total_memory": total_memory,
            "used_memory": used_memory,
            "free_memory": free_memory,
            "buffer_cache": buffer_cache,
            "total_swap": total_swap,
            "used_swap": used_swap,
            "free_swap": free_swap
        }
