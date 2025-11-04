# Homework #4 - Time Synchronization Submission

# Student: Alexander Lee

# Class: CYBS 5123

This submission includes all required components for the graduate-level track of the assignment.

## 1. Included Files

1. `sync_time.py`: The Python script that uses worldtimeapi.org to fetch and set the system time.

crontab_entry.txt: The plain-text crontab entry to schedule the script.

analysis_report.md: The graduate-level analysis comparing the API-based approach to traditional NTP.

README.md: This file, explaining the setup and testing process.

2. Setup and Installation

Before the script can run, you must install its dependencies and place it in a known location.

Step 1: Install Dependencies

On your Ubuntu 22 VM, open a terminal and run the following commands to install Python's 'requests' library:

sudo apt-get update
sudo apt-get install python3-pip -y
pip3 install requests


Step 2: Place the Script

Save the sync_time.py file to your home directory (e.g., /home/student/sync_time.py).

Make the script executable:

chmod +x /home/student/sync_time.py


3. How to Get Your Screenshots (Testing)

This is the most important part. You need to show the script working. The easiest way to do this is to manually set your clock to be wrong, then run the script and show it being corrected.

Step 1: Set your system time to be 10 minutes off (BEFORE).

Run this command. It will set your clock to be incorrect.

# Set the time to be 10+ minutes in the past
sudo date -s "10 minutes ago"


Step 2: Check the (wrong) time (BEFORE).

Now, run date. This is your "Before" screenshot.

date


It should show a time that is ~10 minutes in the past.

Step 3: Run the script manually (THE ACTION).

Now, run the script using sudo. The script will detect the 10-minute difference and fix it.

# Make sure to use the absolute path to your script
sudo /usr/bin/python3 /home/student/sync_time.py


The output will look like this. This is your "Running Code" screenshot.

[2025-11-04 12:30:05.123456] Running time synchronization check...
  > API Time (Unix):   1762419015
  > System Time (Unix): 1762418415
  > Time Difference:   600 seconds.
Difference (600s) exceeds threshold (300s).
Attempting to update system time...
Success: System time updated.
STDOUT: Tue Nov  4 12:50:15 CST 2025
------------------------------------------------------------


Step 4: Check the (corrected) time (AFTER).

Immediately run date again. It will now show the correct time, pulled from the API. This is your "After" screenshot.

date


The time will now be correct, matching the "API Time" from the script's output. You have now proven your script works!

4. Final Crontab Setup

After you've tested it and gotten your screenshots, you can set up the crontab to run it automatically.

Open the root user's crontab editor:

sudo crontab -e


Select an editor (like nano, if prompted).

Go to the bottom of the file and paste the line from crontab_entry.txt, making sure the path to your script is correct.

*/30 * * * * /usr/bin/python3 /home/student/sync_time.py >> /var/log/time_sync.log 2>&1


Save and exit the editor.

Your system will now automatically sync its time every 30 minutes. You can check the log file to see it working:

tail -f /var/log/time_sync.log
