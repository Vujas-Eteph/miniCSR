# - IMPORTS -------------------------------------------------------------------
from .free_extractor import FreePatternExtractor
from .uptime_extractor import UptimePatternExtractor
from .ps_extractor import CpuUsageByUserExtractor
from .top_extractor import TopExtractor


# - CLASS ---------------------------------------------------------------------
class CPUWatcher:
    def __init__(self, threshold=1):
        self.threshold = threshold
        self.free_extractor = FreePatternExtractor()
        self.uptime_extractor = UptimePatternExtractor()
        self.cpu_load_extractor = CpuUsageByUserExtractor()
        self.top_load_extractor = TopExtractor()

    def _filter_by_threshold(self, cpu_load_wrt_user):
        """Filter users by CPU load threshold."""
        filtered_cpu_usage = {}
        for user, cpu_load in cpu_load_wrt_user.items():
            if cpu_load > self.threshold:
                filtered_cpu_usage[user] = cpu_load
        return filtered_cpu_usage

    def _normalize_cpu_usage(self, cpu_load_wrt_user, cpu_count):
        normalized_cpu_usage = {}

        for user, cpu_load in cpu_load_wrt_user.items():
            # Normalize the CPU load based on the number of CPUs
            normalized_cpu_usage[user] = cpu_load / cpu_count

        return normalized_cpu_usage

    def get_cpu_statistics(
        self,
        cpu_memory_info,
        cpu_load_info,
        cpu_load_wrt_user_info,
        top_output,
        cpu_count,
        cpu_util_info,
    ):
        cpu_memory = self.free_extractor.get_free_info(cpu_memory_info)
        cpu_load = self.uptime_extractor.get_uptime_info(cpu_load_info)
        cpu_load_wrt_user = self.cpu_load_extractor.get_cpu_usage_by_user(
            cpu_load_wrt_user_info
        )
        cpu_count = int(cpu_count)
        top_cpu_res = self.top_load_extractor.get_cpu_usage_by_user(top_output)

        top_cpu_res.pop("root")

        # Normalize the filtered CPU load by the number of CPUs
        normalized_cpu_load_wrt_user = self._normalize_cpu_usage(
            top_cpu_res, cpu_count
        )

        # Filter CPU usage by the threshold
        filtered_cpu_load_wrt_user = self._filter_by_threshold(
            normalized_cpu_load_wrt_user
        )

        # print("cpu load", cpu_load.get('load_5min')/cpu_count)
        # print(filtered_cpu_load_wrt_user)

        # !WARNING Not clean!
        cpu_util_info = cpu_util_info.split(' - ')
        us_cpu = float(cpu_util_info[0].split(' ')[-1].replace(',', '.'))
        sy_cpu = float(cpu_util_info[1].split(' ')[-1].replace(',', '.'))
        cpu_util = us_cpu + sy_cpu
        cpu_idle = float(cpu_util_info[2].split(' ')[-1].replace(',', '.'))
        wa_cpu = float(cpu_util_info[3].split(' ')[-1].replace(',', '.'))

        cpu_util_distribution = {"us_cpu": round(us_cpu, 2),
                                 "sy_cpu": round(sy_cpu, 2),
                                 "cpu_util": round(cpu_util, 2),
                                 "idle_cpu": round(cpu_idle, 2),
                                 "wait_cpu": round(wa_cpu, 2),
                                 }

        return {
            "cpu_memory": cpu_memory,
            "cpu_load": cpu_load,
            "normalized_cpu_load_wrt_user": filtered_cpu_load_wrt_user,
            "cpu_count": cpu_count,
            "cpu_util_distribution": cpu_util_distribution,
        }
