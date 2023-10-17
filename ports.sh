#!/bin/bash

# Simple script when you can't install the normal utils to see listening tcp ports.
# 

echo "Listening Ports:"

# Function to parse /proc/net/tcp and /proc/net/tcp6 files
parse_proc_net_tcp() {
    local file=$1
    while IFS= read -r line; do
        if [[ $line != sl* ]]; then  # Ignore the header line
            local port=$(echo "$line" | awk '{print $2}' | cut -d':' -f2)
            local state=$(echo "$line" | awk '{print $4}')

            # Check if the state is 0A, which means LISTEN
            if [ "$state" == "0A" ]; then
                # Convert hex port to decimal
                echo "$((16#$port))"
            fi
        fi
    done < "$file"
}

# Parse IPv4 listening ports
parse_proc_net_tcp /proc/net/tcp

# Parse IPv6 listening ports if the tcp6 file is available
if [ -f /proc/net/tcp6 ]; then
    parse_proc_net_tcp /proc/net/tcp6
fi
