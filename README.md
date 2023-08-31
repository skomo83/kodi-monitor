# kodi-monitor
#Monitor port 8080 so that when you connect with the phone app and Kodi is not running, it will start up Kodi.

#This is usefull when you use the Kodi iPhone app.
#run the program by using
python3 monitor-kodi.py --log-level INFO --user USERNAME

#the --user option is required,
#the --log-level is optional as the default is set to INFO

#Change the kodi desktop icon to call kodistart.sh so that way the port bound to 8080 by the script gets released if 
#starting Kodi from the desktop icon.
#modify the kodi-monitor.service file to point to the correct location for the scripts
#copy kodi-monitor.service to /etc/systemd/service
sudo systemctl daemon-reload
sudo systemctl start kodi-monitor.service

#test that it works.
#once working, enable the service using 
sudo systemctl enable kodi-monitor.service

#enjoy
