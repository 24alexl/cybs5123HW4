# Homework #4 - Time Synchronization Submission

# Student: Alexander Lee

# Class: CYBS 5123

This submission includes all required components for the graduate-level track of the assignment.

## 1. Included Files

1. `sync_time.py`: The Python script that uses worldtimeapi.org to fetch and set the system time.

2. `crontab_entry.txt`: The plain-text crontab entry to schedule the script.

3. `README.md`: This file, explaining the setup and testing process.

## 2. Setup and Installation

Before the script can run, you must install its dependencies and place it in a known location.

### Step 1: Install Dependencies

On your Ubuntu 22 VM, open a terminal and run the following commands to install Python's 'requests' library:
```
sudo apt-get update
sudo apt-get install python3-pip -y
pip3 install requests
```

### Step 2: Place the Script

Save the sync_time.py file to your home directory (e.g., /home/netadmin/sync_time.py).

Make the script executable:
```
chmod +x /home/netadmin/sync_time.py
```

## 3. Final Crontab Setup

After you've tested it and gotten your screenshots, you can set up the crontab to run it automatically.

1. Open the root user's crontab editor:
```
sudo crontab -e
```

2. Select an editor (like nano, if prompted).

3. Go to the bottom of the file and paste the line from crontab_entry.txt, making sure the path to your script is correct.
```
*/30 * * * * /usr/bin/python3 /home/netadmin sync_time.py >> /var/log/time_sync.log 2>&1
```
4. Save and exit editor.
