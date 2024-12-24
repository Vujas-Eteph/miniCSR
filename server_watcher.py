# - IMPORTS -------------------------------------------------------------------
import time
import numpy as np

from gpu_monitor.gpu_watcher import GPUWatcher
from cpu_monitor.cpu_watcher import CPUWatcher
from disk_space_monitor.disk_space_watcher import DiskSPaceWatcher


# - CLASSES -------------------------------------------------------------------
class ServerWatcher():
    def __init__(self, WATCH_GPU=True, WATCH_CPU=True, WATCH_DISK_SPACE=True):
        self.gpu_watcher = GPUWatcher()
        self.cpu_watcher = CPUWatcher()
        self.disk_space_watcher = DiskSPaceWatcher()
        self.WATCH_GPU = WATCH_GPU
        self.WATCH_CPU = WATCH_CPU
        self.WATCH_DISK_SPACE = WATCH_DISK_SPACE

    def _get_timestamp(self):
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    def _get_gpu_statistics(self, output):
        return self.gpu_watcher.get_gpu_statistics(output)

    def _get_cpu_statistics(self, outputs):
        return self.cpu_watcher.get_cpu_statistics(*outputs)
    
    def _get_disk_space_statistics(self, output):
        return self.disk_space_watcher.get_disk_space_statistics(output)

    def get_server_statistics(self, hostname, gpu_output=None,
                              cpu_output=None, disk_space_output=None):
        server_stats = {"timestamp": self._get_timestamp(),
                        "hostname": hostname,
                        # "hostname": "hostname",  # Only during tests
                        }

        if self.WATCH_GPU and gpu_output:
            server_stats["gpus"] = self._get_gpu_statistics(gpu_output)
            list_gpu_mem_used = [server['memory_used'] for server in server_stats["gpus"]]
            list_gpu_mem_tot = [server['memory_total'] for server in server_stats["gpus"]]
            list_gpu_util = [server['gpu_utilization'] for server in server_stats["gpus"]]
            server_stats["gpus_list_gpu_mem_used"] = list_gpu_mem_used
            server_stats["gpus_list_gpu_gpu_util"] = list_gpu_util
            server_stats["avg_gpu_mem_used"] = round(np.average(np.array(list_gpu_mem_used)/np.array(list_gpu_mem_tot))*100, 2)
            server_stats["avg_gpu_mem_util"] = round(np.average(np.array(list_gpu_util)), 2)

        if self.WATCH_CPU and cpu_output:
            server_stats["cpus"] = self._get_cpu_statistics(cpu_output)

        if self.WATCH_DISK_SPACE and disk_space_output:
            server_stats["disk_space"] = self._get_disk_space_statistics(disk_space_output)
            # print(self._get_disk_space_statistics(disk_space_output)['dataframe'])
        return server_stats
