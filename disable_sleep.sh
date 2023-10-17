#!/bin/bash

# Disable screensaver and power management
xset s off
xset -dpms


# Keep the script running
while true; do
    sleep 60   # Sleep for 1 minute before checking again
done
