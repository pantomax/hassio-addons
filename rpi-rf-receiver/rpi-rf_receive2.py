#!/usr/bin/env python3

import argparse
import signal
import sys
import time
import logging
import io, os, datetime, shutil

mosquitto_address = "192.168.1.100"
mosquitto_port = "1883"
mosquitto_user = "homeassistant"
mosquitto_password = "REDACTED" 

from rpi_rf import RFDevice

rfdevice = None
rfdevice2 = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=27,
                    help="433 MHz GPIO pin (Default: 27)")
parser.add_argument('-g', dest='gpio2', type=int, default=22,
                    help="434 Mhz GPIO pin (Default: 22)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)

rfdevice = RFDevice(args.gpio)
rfdevice2 = RFDevice(args.gpio2)

rfdevice.enable_rx()
rfdevice2.enable_rx()

timestamp = None
timestamp2 = None

logging.info("Listening for codes on GPIO " + str(args.gpio) + " and GPIO " + str(args.gpio2))
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logging.info(str(rfdevice.rx_code) +
                     " [pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
        os.system("mosquitto_pub -h " + mosquitto_address + " -p " + mosquitto_port + " -t 'sensors/rf/receiver' -u " + mosquitto_user + " -P " + mosquitto_password + " -m " + str(rfdevice.rx_code))
    if rfdevice2.rx_code_timestamp != timestamp2:
        timestamp2 = rfdevice2.rx_code_timestamp
        logging.info(str(rfdevice2.rx_code) +
                     " [pulselength " + str(rfdevice2.rx_pulselength) +
                     ", protocol " + str(rfdevice2.rx_proto) + "]")
        os.system("mosquitto_pub -h " + mosquitto_address + " -p " + mosquitto_port + " -t 'sensors/rf/receiver2' -u " + mosquitto_user + " -P " + mosquitto_password + " -m " + str(rfdevice2.rx_code))
    time.sleep(0.01)
rfdevice.cleanup() 
