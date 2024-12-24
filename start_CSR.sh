#!/bin/bash

# Trap to kill all background processes on script exit
trap "kill 0" EXIT

# Prompt for the password once at the beginning of the script
read -sp "Enter your password: " PASSWORD
echo  # Add a newline after the password prompt for better formatting

# Function to run the monitoring script with periodic restart
restart_monitoring() {
    while true; do
        # Use the password to run the monitoring script
        python3 monitoring.py -r 3600 -s 5 -p "$PASSWORD"  # Runs for 1 hour then restarts
        sleep 5  # Wait for 5 sec before restart
    done
}

# Start the monitoring script in a loop
restart_monitoring &

# Start the Gunicorn server
gunicorn -w 4 -b 0.0.0.0:1990 app:app &

# Wait for all background processes to finish
wait
