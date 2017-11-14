# RPI RF Receiver

This addon is made to make the rpi-rf receiver script run in background of you hassio

1. Install the addon (it take 5-10 minutes to intall).

2. Copy "rpi-rf_receive.py" in the "share" share of your hass.io.

3. Edit "rpi-rf_receive.py" adding your mosquitto address, port, user and  password. 

4. Start the addon 

5. Add this sensor to read the codes in your hassio:

sensor:
  - platform: mqtt
  
    state_topic: "sensors/rf/receiver"
    
    name: "RF Receiver"
