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
    rfdevice2.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433 GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=27, help="433 MHz GPIO pin (Default: 27)")
args = parser.parse_args()
parser2 = argparse.ArgumentParser(description='Receives a decimal code via a 434 GPIO device')
parser2.add_argument('-g', dest='gpio', type=int, default=22, help="434 Mhz GPIO pin (Default: 22)")
args2 = parser2.parse_args()

signal.signal(signal.SIGINT, exithandler)

rfdevice = RFDevice(args.gpio)
rfdevice2 = RFDevice(args2.gpio)

rfdevice.enable_rx()
rfdevice2.enable_rx()

timestamp = None
timestamp2 = None

logging.info("Listening for codes on GPIO " + str(args.gpio) + " and GPIO " + str(args2.gpio))
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        logging.info(str(rfdevice.rx_code) +
                     " [GPIO 27, pulselength " + str(rfdevice.rx_pulselength) +
                     ", protocol " + str(rfdevice.rx_proto) + "]")
        os.system("mosquitto_pub -h " + mosquitto_address + " -p " + mosquitto_port + " -t 'sensors/rf/receiver' -u " + mosquitto_user + " -P " + mosquitto_password + " -m " + str(rfdevice.rx_code))
    if rfdevice2.rx_code_timestamp != timestamp2:
        timestamp2 = rfdevice2.rx_code_timestamp
        logging.info(str(rfdevice2.rx_code) +
                     " [GPIO 22, pulselength " + str(rfdevice2.rx_pulselength) +
                     ", protocol " + str(rfdevice2.rx_proto) + "]")
        os.system("mosquitto_pub -V mqttv311 -h " + mosquitto_address + " -p " + mosquitto_port + " -t 'sensors/rf/receiver2' -u " + mosquitto_user + " -P " + mosquitto_password + " -m " + str(rfdevice2.rx_code))
    time.sleep(0.01)
rfdevice.cleanup()
rfdevice2.cleanup()
