#!/usr/bin/env python3

"""
================================================================================
CYBS 5123 - Network Time Synchronization Script (Graduate Version)
================================================================================
This script synchronizes the system time using the 'worldtimeapi.org'
HTTPS API, as required for the graduate-level assignment.

It is designed to be run as root or with sudo privileges to have
permission to change the system time.

It performs the following steps:
1.  Fetches the current UTC time from worldtimeapi.org.
2.  Parses the response to get the 'unixtime' (seconds since epoch).
3.  Gets the current system time as a UTC timestamp.
4.  Compares the two timestamps.
5.  If the difference exceeds 300 seconds (5 minutes), it updates
    the system time using 'date -s @<unixtime>'.
6.  Prints the status (updated, or already in sync).
"""

import requests
import datetime
import subprocess
import sys

# Configuration
API_URL = "https://worldtimeapi.org/api/timezone/Etc/UTC"
MAX_TIME_DIFFERENCE_SECONDS = 300  # 5 minutes

def get_api_time():
    """
    Fetches the current UTC time from worldtimeapi.org.
    Returns the 'unixtime' as an integer, or None if an error occurs.
    """
    try:
        response = requests.get(API_URL, timeout=10)
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        data = response.json()
        
        if 'unixtime' in data:
            return int(data['unixtime'])
        else:
            print(f"Error: 'unixtime' not found in API response.", file=sys.stderr)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to time API: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        return None

def get_system_time_unix():
    """
    Returns the current system time as a UTC Unix timestamp (integer).
    """
    # Get current time, aware of UTC
    system_time_utc = datetime.datetime.now(datetime.timezone.utc)
    # Convert to Unix timestamp (seconds since epoch)
    return int(system_time_utc.timestamp())

def set_system_time(unixtime):
    """
    Sets the system time using 'date -s @<timestamp>'.
    Requires sudo/root privileges.
    """
    try:
        # Format the command: ['sudo', 'date', '-s', '@1678886400']
        # We don't need 'sudo' here if the script is run *by* sudo or root cron
        command = ["date", "-s", f"@{unixtime}"]
        
        # We use 'subprocess.run' which is the modern standard.
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        
        print(f"Success: System time updated.")
        print(f"STDOUT: {result.stdout.strip()}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to set system time. Do you have root privileges?", file=sys.stderr)
        print(f"COMMAND: {' '.join(command)}", file=sys.stderr)
        print(f"STDERR: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print(f"Error: 'date' command not found. This script is intended for a Linux environment.", file=sys.stderr)
        return False

def main():
    """
    Main function to run the time synchronization logic.
    """
    print(f"[{datetime.datetime.now()}] Running time synchronization check...")
    
    # 1. Get time from API
    api_time_unix = get_api_time()
    if api_time_unix is None:
        print("Failed to retrieve API time. Exiting.")
        return

    # 2. Get system time
    system_time_unix = get_system_time_unix()
    
    print(f"  > API Time (Unix):   {api_time_unix}")
    print(f"  > System Time (Unix): {system_time_unix}")

    # 3. Compare times
    difference = abs(api_time_unix - system_time_unix)
    print(f"  > Time Difference:   {difference} seconds.")

    # 4. Update if necessary
    if difference > MAX_TIME_DIFFERENCE_SECONDS:
        print(f"Difference ({difference}s) exceeds threshold ({MAX_TIME_DIFFERENCE_SECONDS}s).")
        print("Attempting to update system time...")
        set_system_time(api_time_unix)
    else:
        print("Time is already in sync. No update needed.")
    
    print("-" * 60)

if __name__ == "__main__":
    main()

