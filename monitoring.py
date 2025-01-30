# - HELP ----------------------------------------------------------------------
# https: https://stackoverflow.com/questions/10175812/how-to-generate-a-self-signed-ssl-certificate-using-openssl


# - IMPORTS -------------------------------------------------------------------
import threading
import time
import pandas as pd
from tabulate import tabulate
import datetime
import json
import yaml

from config.config import arg_parser
from server_watcher import ServerWatcher
from ssh_utils.connection_manager import ConnectionManagerViaSSH
from ssh_utils.cmd_manager import ManageCmdsToHosts


# - CONSTANTS -----------------------------------------------------------------
# Global variables
latest_result = "No data yet"
latest_result_detailed = "No data yet"
latest_result_detailed_space = "No data yet"

# Read server aliases
with open("config/server_names.yaml") as f:
    GPU_SERVER_ALIASES = yaml.safe_load(f)["GPU_SERVER_ALIASES"]


# - FUNCTIONS -----------------------------------------------------------------
def calculate_average_utilization(server_data, server_alias):
    """Compute some statistics"""
    # Create dicts
    server_stats = {}
    server_stats_detailed = {}
    disk_stats_detailed = {}

    # Iterate over each server in the results
    # to extract GPU, CPU, and Disk Space details
    cpu_info = server_data["cpus"]
    disk_space = server_data["disk_space"]

    # GPU and CPU Statistics
    server_stats[server_alias] = {
        "Avg. GPU Memory (%)": server_data["avg_gpu_mem_used"],
        "Avg. GPU Utilization (%)": server_data["avg_gpu_mem_util"],
        "Active Users": list(cpu_info["normalized_cpu_load_wrt_user"].keys()),
        "Total CPU Load (%)": round(
            (
                cpu_info.get("cpu_load").get("load_5min")
                / cpu_info.get("cpu_count")
            )
            * 100,
            2,
        ),
    }
    # Detailled GPU Statistics
    server_stats_detailed[server_alias] = {
        "GPU Memory (MiB)": server_data["gpus_list_gpu_mem_used"],
        "GPU Utilization (%)": server_data["gpus_list_gpu_gpu_util"],
        "Temperature (C)": server_data["gpus_list_gpu_temperature"],
        "GPU Fan (%)": server_data["gpus_list_gpu_fan_speed"],
        "Power Usage (W)": server_data["gpus_list_gpu_power_used"],
    }
    # Disk Space Statistics
    disk_stats_detailed[server_alias] = {
        "Average Disk Space Used (%)": disk_space["Avg Use %"],
        "Total Disk Space Used (TB)": disk_space["Tot Used"],
        "Total Disk Space Avail (TB)": disk_space["Tot Avail"],
    }

    return server_stats, server_stats_detailed, disk_stats_detailed


def thread_server_moni(
    START_TIME,
    HOURS_TO_RUN,
    cmd_manager,
    GPU_server_alias,
    server_watcher,
    SLEEP,
    lock,
    barrier,
    shared_server_stats,
    shared_server_stats_detailed,
    shared_server_disk_detailed,
):
    """Monitor a GPU server with one Thread"""

    global latest_result, latest_result_detailed, latest_result_detailed_space

    while time.time() - START_TIME < HOURS_TO_RUN:
        # GPU, CPU, and Disk Space Monitoring
        host_output, _ = cmd_manager.execute_cmd_on_host(
            GPU_server_alias, "nvidia-smi"
        )
        cpu_stats = [
            cmd_manager.execute_cmd_on_host(GPU_server_alias, cmd)[0]
            for cmd in [
                "free",
                "uptime",
                "ps -eo user,pcpu",
                "top -b -n 1 | awk 'NR>7 {cpu[$2]+=$9} END {for (u in cpu) print u, cpu[u]}'",
                "nproc",
            ]
        ]
        disk_space_stats = [
            cmd_manager.execute_cmd_on_host(GPU_server_alias, cmd)[0]
            for cmd in ["df | grep -E '^/dev/' | grep -vE 'boot|tmpfs'"]
        ]

        # Thread-safe write to results
        gpac_msg = server_watcher.get_server_statistics(
            GPU_server_alias,
            gpu_output=host_output,
            cpu_output=cpu_stats,
            disk_space_output=disk_space_stats,
        )bbb

        server_stats, detailled_server_stats, disk_stats_detailed = (
            calculate_average_utilization(gpac_msg, GPU_server_alias)
        )

        with lock:
            shared_server_stats[GPU_server_alias] = server_stats[
                GPU_server_alias
            ]
            shared_server_stats_detailed[GPU_server_alias] = (
                detailled_server_stats[GPU_server_alias]
            )
            shared_server_disk_detailed[GPU_server_alias] = (
                disk_stats_detailed[GPU_server_alias]
            )

        # Synchronize threads
        try:
            barrier.wait()
        except threading.BrokenBarrierError:
            print(f"Barrier broken in thread {GPU_server_alias}")

        time.sleep(SLEEP)


# - MAIN ----------------------------------------------------------------------
def main():
    args = arg_parser()
    HOURS_TO_RUN = args.run
    SLEEP = args.sleep
    START_TIME = time.time()

    global latest_result, latest_result_detailed, latest_result_detailed_space

    server_watcher = ServerWatcher()
    host_manager = ConnectionManagerViaSSH(args.password)
    cmd_manager = ManageCmdsToHosts(host_manager)

    shared_server_stats = {}
    shared_server_stats_detailed = {}
    shared_server_disk_detailed = {}
    results_lock = threading.Lock()

    def update_latest_results():
        global \
            latest_result, \
            latest_result_detailed, \
            latest_result_detailed_space

        with results_lock:
            # Update the global variable for Flask in a thread-safe manner
            current_time = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Convert shared dictionaries to DataFrames
            df_stats = pd.DataFrame.from_dict(
                shared_server_stats, orient="index"
            )
            df_stats_detailed = pd.DataFrame.from_dict(
                shared_server_stats_detailed, orient="index"
            )
            df_disk_space_detailed = pd.DataFrame.from_dict(
                shared_server_disk_detailed, orient="index"
            )

            # Sort the DataFrames by index (server names) alphabetically
            df_stats_sorted = df_stats.sort_index()
            df_stats_detailed_sorted = df_stats_detailed.sort_index()
            df_disk_space_detailed_sorted = df_disk_space_detailed.sort_index()

            # Use tabulate to create the tables
            latest_result = f"Time Stamp: {current_time}\n"  # Add timestamp
            latest_result += tabulate(
                df_stats_sorted, headers="keys", tablefmt="grid"
            )

            latest_result_detailed = (
                f"Time Stamp: {current_time}\n"  # Add timestamp
            )
            latest_result_detailed += tabulate(
                df_stats_detailed_sorted, headers="keys", tablefmt="grid"
            )

            latest_result_detailed_space = (
                f"Time Stamp: {current_time}\n"  # Add timestamp
            )
            latest_result_detailed_space += tabulate(
                df_disk_space_detailed_sorted, headers="keys", tablefmt="grid"
            )

            payload = {
                "stats": latest_result,
                "detailed_stats": latest_result_detailed,
                "disk_stats": latest_result_detailed_space,
            }

            with open("data.json", "w") as file:
                json.dump(payload, file, indent=4)

    try:
        # Establish SSH connections
        for GPU_server_alias in GPU_SERVER_ALIASES:
            host_manager.add_connection(GPU_server_alias)
            host_manager.connect_to_server(GPU_server_alias)
        valid_GPU_SERVER = host_manager.check_current_servers_alive()

        # Create a barrier with the action function
        barrier = threading.Barrier(
            len(valid_GPU_SERVER), action=update_latest_results
        )
        threads = []

        # Start monitoring threads
        for GPU_server_alias in valid_GPU_SERVER:
            thread = threading.Thread(
                target=thread_server_moni,
                args=(
                    START_TIME,
                    HOURS_TO_RUN,
                    cmd_manager,
                    GPU_server_alias,
                    server_watcher,
                    SLEEP,
                    results_lock,
                    barrier,
                    shared_server_stats,
                    shared_server_stats_detailed,
                    shared_server_disk_detailed,
                ),
            )
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    except KeyboardInterrupt:
        print("\nCtrl+C detected. Terminating gracefully...")

    finally:
        # Ensure that all SSH connections are closed on exit
        print("Closing all SSH connections...")
        host_manager.close_all_connections()
        print("SSH connections closed.")
        latest_result = "SSH connections closed"


if __name__ == "__main__":
    main()
