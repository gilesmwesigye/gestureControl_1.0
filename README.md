# gestureControl_1.0
 
chmod +x disable_sleep.sh

Create a systemd service file for your script. Create a new file with a .service extension, for example, disable_sleep.service, and open it in a text editor:

sudo nano /etc/systemd/system/disable_sleep.service

Add the following content to the disable_sleep.service file:

[Unit]
Description=Disable Sleep Service
After=network.target

[Service]
ExecStart=/path/to/disable_sleep.sh
StandardOutput=null

[Install]
WantedBy=default.target

Replace /path/to/disable_sleep.sh with the actual path to your disable_sleep.sh script.

Save the file and exit the text editor.

Reload the systemd manager configuration:

sudo systemctl daemon-reload

Enable the service to run on boot:

sudo systemctl enable disable_sleep.service
