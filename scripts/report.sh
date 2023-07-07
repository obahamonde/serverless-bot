#!/bin/bash

# Get the total available memory
total_memory=$(free -k | awk '/^Mem:/ {print $2}')

# Get the memory usage percentage
memory_usage_percentage=$(free -k | awk '/^Mem:/ {printf("%.2f", ($3/$2) * 100)}')

# Get the top three processes by memory usage
top_processes=$(ps -eo pid,comm,%mem --sort=-%mem | head -n 4 | awk 'NR>1 {print $0}')

# Extract the PIDs of the top three processes
pids=$(echo "$top_processes" | awk '{print $1}')

# Initialize variable to store port information
port_info=""

# Iterate through the PIDs and find associated ports
for pid in $pids; do
    ports=$(sudo lsof -i -P -n -p "$pid" | awk '/LISTEN/ {print $9}')
    port_info+="PID: $pid, Ports: $ports"$'\n'
done

# Output the report
echo "Memory Usage: $memory_usage_percentage%"
echo "Top 3 Processes:"
echo "$top_processes"
echo
echo "Port Information:"
echo "$port_info"
