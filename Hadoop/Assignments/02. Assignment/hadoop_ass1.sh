#!/bin/bash


# Start SH services
start-dfs.sh 2>/dev/null
echo "Hadoop Started Successfully" | lolcat

# Creating LogAnalytics
hdfs dfs -mkdir -p /user/S-M-Y-A/LogAnalytics 2>/dev/null

# Copy the entire log_staging to LogAnalytics directory in HDFS.
hdfs dfs -copyFromLocal /home/acts/Mohit/PGD-HPCSA/Hadoop/Assignments/log_staging /user/S-M-Y-A/LogAnalytics/ 2>/dev/null

# Create a new empty directory inside HDFS at /user/<your_username>/LogAnalytics/ named reports.
hdfs dfs -mkdir /user/S-M-Y-A/LogAnalytics/reports 2>/dev/null

# Move the click_data_01.csv file (which is now in HDFS) from its current location into the reports directory you just created.
hdfs dfs -mv /user/S-M-Y-A/LogAnalytics/log_staging/clickstream/click_data_01.csv /user/S-M-Y-A/LogAnalytics/reports 2>/dev/null



echo ""
# Part 3: Verification and File Information


# 1. Display the contents of the click_data_01.csv file (from its new location in HDFS) directly to your terminal.
echo "The Content of CSV file"
hdfs dfs -cat /user/S-M-Y-A/LogAnalytics/reports/click_data_01.csv 2>/dev/null
echo ""


# 2. List the contents of your /user/<your_username>/LogAnalytics directory in HDFS to show the new structure (including log_staging and reports).
echo "The Content of LogAnalytics"
hdfs dfs -ls /user/S-M-Y-A/LogAnalytics 2>/dev/null
echo ""

# 3. Get a "human-readable" summary of the total disk space used by the entire /user/<your_username>/LogAnalytics directory in HDFS.
echo "Disk Usage of LogAnalytics"
hdfs dfs -du -s -h /user/S-M-Y-A/LogAnalytics 2>/dev/null
echo ""

# 4. Show the last 50 bytes of the server_log_01.txt file. (Note: Since the file is empty, what do you expect to see?)
echo "Last 50 bytes of Server log 01"
hdfs dfs -tail /user/S-M-Y-A/LogAnalytics/log_staging/raw_logs/server_log_01.txt 2>/dev/null
echo ""





# Part 4: Managing File Permissions

# 1. Policy 1: The raw_logs directory contains sensitive data. It should only be accessible by the owner (you).

hdfs dfs -chmod 700 /user/S-M-Y-A/LogAnalytics/log_staging/raw_logs 2>/dev/null

# 2. Policy 2: The reports directory contains data for the data science team.

hdfs dfs -chmod 755 /user/S-M-Y-A/LogAnalytics/reports 2>/dev/null


# 3. Display a long listing of the /user/<your_username>/LogAnalytics/ directory and its contents to prove that the new permissions are set correctly.
echo "Long List of LogAnalytics with Changed Permissions"
hdfs dfs -ls /user/S-M-Y-A/LogAnalytics/ 2>/dev/null
echo ""

