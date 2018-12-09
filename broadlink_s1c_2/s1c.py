import broadlink
import time, os

mosquitto_address = "x.x.x.x" # change the ip address, user name and password for your mosquitto server
mosquitto_port = "xxxx"
mosquitto_user = "x"
mosquitto_password = "x"
broadlink_s1c_ip = "x.x.x.x" # Change to your S1C IP Address and S1C Mac Address
broadlink_s1c_mac = "xxxxxxxxxxxx"

devices = broadlink.S1C(host=(broadlink_s1c_ip,80), mac=bytearray.fromhex(broadlink_s1c_mac)) # Change to your S1C IP Address and S1C Mac Address
devices.auth()

sens = devices.get_sensors_status()
old = sens


while 1:
	try:
		sens = devices.get_sensors_status()
		for i, se in enumerate(sens['sensors']):
			if se['status'] != old['sensors'][i]['status']:
				sName = se['name']
				sType = se['type']
				if sType == "Door Sensor" and str(se['status']) == "0" or sType == "Door Sensor" and str(se['status']) == "128": # Instead of sType you can test for sName in case you have multiple sensors
					print time.ctime() + ": Door closed: " + str(se['status'])
					os.system("mosquitto_pub -h mosquitto_address -p mosquitto_port -t 'sensors/s1c/entrance_door' -u mosquitto_user -P mosquitto_password -m " + "Closed") 
				elif sType == "Door Sensor" and str(se['status']) == "16" or sType == "Door Sensor" and str(se['status']) == "144":
					print time.ctime()  +": Door opened: " + str(se['status'])
					os.system("mosquitto_pub -h mosquitto_address -p mosquitto_port -t 'sensors/s1c/entrance_door' -u mosquitto_user -P mosquitto_password -m " + "Open")
				elif sType == "Door Sensor" and str(se['status']) == "48":
					print time.ctime()  +": Door Sensor tampered: " + str(se['status'])
					os.system("mosquitto_pub -h mosquitto_address -p mosquitto_port -t 'sensors/s1c/entrance_door' -u mosquitto_user -P mosquitto_password -m " + "Tampered")
				elif sType == "Motion Sensor" and str(se['status']) == "0" or sType == "Motion Sensor" and str(se['status']) == "128":
					print time.ctime()  +": No Motion: " + str(se['status'])
					os.system("mosquitto_pub -h mosquitto_address -p mosquitto_port -t 'sensors/s1c/motion_sensor' -u mosquitto_user -P mosquitto_password -m " + "No_motion")
				elif sType == "Motion Sensor" and str(se['status']) == "16":
					print time.ctime()  +": Motion Detected: " + str(se['status'])
					os.system("mosquitto_pub -h mosquitto_address -p mosquitto_port -t 'sensors/s1c/motion_sensor' -u mosquitto_user -P mosquitto_password -m " + "Motion_Detected")
				elif sType == "Motion Sensor" and str(se['status']) == "32":
					print time.ctime()  +": Motion Sensor Tampered: " + str(se['status'])
					os.system("mosquitto_pub -h mosquitto_address -p mosquitto_port -t 'sensors/s1c/motion_sensor' -u mosquitto_user -P mosquitto_password -m " + "Tampered")
				old = sens
	except:
		continue

