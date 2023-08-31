!#!/bin/bash

# Restart the target service and start kodi
# add this to sudoers file
# username ALL=(ALL) NOPASSWD: /bin/systemctl restart kodi-monitor.service

sudo systemctl restart kodi-remote.service && kodi

