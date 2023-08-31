# kodi-remote-start

kodi-remote-start will monitor port 8080 so that when you connect with the phone app and Kodi is not running, it will start up Kodi.


## Usage
```bash
python3 remote-kodi.py --log-level INFO --user USERNAME
```

the --user option is required,

the --log-level is optional as the default is set to INFO

the logs are stored at the same location as remote-kodi.py

Edit the kodi.desktop icon file to call kodistart.sh so the port bound to 8080 by the script gets released when starting Kodi from the desktop icon.

Change the Exec line to match where you have the files
```nano 
Exec=/home/USERNAME/kodi-remote/kodistart.sh
```

modify the kodi-monitor.service file to point to the correct location for the scripts

this is where you can set the logging detail and you must set your linux login username
```nano 
ExecStart=/usr/bin/python3 /home/USERNAME/kodi-remote/remote-kodi.py --log-level INFO --user USERNAME
```

copy kodi-monitor.service to /etc/systemd/service
```bash
sudo cp kodi-remote.service /etc/systemd/service
sudo systemctl daemon-reload
sudo systemctl start kodi-remote.service
```

add your user to sudoers 
```bash
USERNAME ALL=(ALL) NOPASSWD: /bin/systemctl restart kodi-remote.service
```


test that it works.
once working, enable the service using 
```bash
sudo systemctl enable kodi-remote.service
```

enjoy
