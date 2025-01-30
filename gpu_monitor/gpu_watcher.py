# - IMPORTS -------------------------------------------------------------------
from .nvidia_smi_extractor import NvidiaSmiPatternExtractor


# - CLASSES -------------------------------------------------------------------
class GPUWatcher(NvidiaSmiPatternExtractor):
    def _get_nvidia_smi_info(self, output):
        gpu_names = self._get_gpu_names(output)
        fan_temp_perf = self._get_fan_temp(output)
        memory_loads = self._get_memory_load(output)
        gpu_utilization = self._get_gpu_utilization(output)

        return gpu_names, fan_temp_perf, memory_loads, gpu_utilization

    def get_gpu_statistics(self, output):
        gpu_names, fan_temp_perf, memory_loads, gpu_utilization = (
            self._get_nvidia_smi_info(output)
        )

        gpus_statistics = []
        for idx, (gpu_id, gpu_name) in enumerate(gpu_names):
            # Quick fix when a GPU is read wrongly so that the server still runs
            try:
                fan, temp, perf, power_usage, power_cap = fan_temp_perf[idx]
            except IndexError:
                fan, temp, perf, power_usage, power_cap = -1, -1, -1, -1, -1

            memory_used, memory_total = memory_loads[idx]
            gpu_util = gpu_utilization[idx]

            gpus_statistics.append(
                {  # "Units"
                    "gpu_id": gpu_id.strip(),
                    "gpu_name": gpu_name.strip(),
                    # ! Replace the  with None in later versions
                    "fan_speed": int(fan) if fan != "N/A" else 0,  # %
                    "temperature": int(temp),  # Celsius
                    "performance": perf,
                    "power_used": int(power_usage),  # Watts
                    "power_total": int(power_cap),  # Wattss
                    "memory_used": int(memory_used),  # MiB
                    "memory_total": int(memory_total),  # MiB
                    "gpu_utilization": int(gpu_util),  # in %
                }
            )

        return gpus_statistics
