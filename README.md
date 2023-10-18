# gestureControl_1.0
Making Script Executable
chmod +x disable_sleep.sh


Running Script on boot
Method 1: Using systemd

systemd is the init system used by Ubuntu and most other modern Linux distributions. It provides a powerful and flexible way to manage services and other system tasks, including running scripts on boot.

To run a script on boot using systemd, you'll need to create a systemd service unit file. This file tells systemd how to run your script, including when to run it and what user to run it as.

Here's an example of a systemd service unit file for a script called disable_sleep.sh:

[Unit]
Description=My Script
After=network.target

[Service]
Type=simple
ExecStart=/path/to/myscript.sh

[Install]
WantedBy=multi-user.target
Save this file as /etc/systemd/system/myscript.service. Then, reload systemd and enable the service:

sudo systemctl daemon-reload
sudo systemctl enable myscript.service
The next time you reboot your system, systemd will run your script.
