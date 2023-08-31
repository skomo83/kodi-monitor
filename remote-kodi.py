#!/usr/bin/python3

import argparse
import logging
import os
import socket
import subprocess
import sys
import time

import psutil

logger = logging.getLogger(__name__)

class KodiRemote:
    def __init__(self, host, port, log_level, kodi_user):
        self.host = host
        self.port = port
        self.sock = None
        self.socket_setup = False 
        self.log_level = log_level
        self.kodi_user = kodi_user
        self.setup_logging()

    def setup_logging(self):
        try:
            logging.basicConfig(filename='kodi_remote.log', level=self.log_level,
                            format='%(asctime)s - %(levelname)s - %(message)s')
        except Exception as e:
            logger.error(f"An error occurred while setting up the logger: {e}")
            sys.exit(1)        

    def is_kodi_running(self):
        wanted_process = 'kodi.bin'
        for process in psutil.process_iter(attrs=['pid', 'name']):
            if process.info['name'] == wanted_process:
                logging.debug(f"{wanted_process} is already running")
                return True
        logging.debug(f"{wanted_process} is not running")
        return False

    def start_kodi(self):
        logging.debug(f"Starting Kodi")
        display = ":0"

        if self.sock:
             self.close_socket()
        
        if not self.is_kodi_running():
            logging.info(f"Starting Kodi for user {self.kodi_user} on display {display} ")
            
            try:
                process = subprocess.Popen(["sudo", "-u", self.kodi_user, f"DISPLAY={display}", "kodi"],
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       universal_newlines=True)
                
                stdout, stderr = process.communicate()
                if stdout:
                    logging.debug(f"Kodi stdout: {stdout}")
                if stderr:
                    logging.error(f"Kodi stderr: {stderr}")

            except Exception as e:
                logging.error(f"Error starting Kodi: {e}")
            
            #subprocess.Popen(["sudo", "-u", self.kodi_user, f"DISPLAY={display}", "kodi"])


    def setup_socket(self):
        logging.debug("Setting up the socket")
        if not self.socket_setup:  # Check the flag
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.sock.bind((self.host, self.port))
                self.sock.listen(1)
                logging.debug(f"Setting up socket listen on port {self.port}")
            except OSError as e:
                if e.errno == 98:
                    logging.warning(f"Port {self.port} is already in use.")
            else:
                self.socket_setup = True  # Set the flag
                logging.debug(f"Socket is open on port {self.port}")
    
    def close_socket(self):
        logging.debug("Closing down the socket")        
        try:
            self.sock.close()
        except Exception as e:
            logging.warning("Failed to close socket: {e}")    
        else:
            self.socket_setup = False
            logging.debug("Socket is closed on port {self.port}")    


    def main_loop(self):
        try:
            while True:
                if not self.is_kodi_running():
                    if self.socket_setup:
                        logging.info(f"Waiting for packet on port {self.port}...")
                        conn, addr = self.sock.accept()
                        logging.info(f"Packet detected from {addr}")
                        if conn:
                            conn.close()
                            self.close_socket()
                        self.start_kodi()
                    else:
                        self.setup_socket() 
                time.sleep(10)                
            logging.warning(f"Exited the Main 'while True' Loop\n")   
        
        except KeyboardInterrupt:
            logging.info("Keyboard interrupt detected")
            self.close_socket()
            logging.info(f"Stopped the Kodi Remote Monitor\n")
        
        else:
            logging.warning(f"Exited via the Main Try Else block\n")       

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Kodi Monitor Script')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='INFO', help='Change the logging level, default is INFO')
    parser.add_argument('--user', help='Set the username that kodi needs to run as')
    
    args = parser.parse_args()
    
    if not args.user:
        logging.error("Error: User cannot be left blank.")
        sys.exit(1)
    
    remote = KodiRemote(host='0.0.0.0', port=8080, log_level=args.log_level, kodi_user=args.user)
    logging.info(f"")
    user = os.getenv("USER")
    if not user:
        user = "systemd"
    logging.info(f"Starting the Kodi Remote Monitor by user : {user}")   
    logging.debug(f"Logging level is '{args.log_level}' and the kodi user is '{args.user}'")   
    remote.main_loop()
    
