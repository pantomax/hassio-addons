# RPI RF Receiver

Since HASSIO removes raw access to RaspberryPi GPIO pins, This addon allows rpi-rf receiver script run in background of you hassio and sends all received RF codes back to HASSIO via MQTT. This enables you to create Switches, Trigger actions, etc from RF Codes received.

PreRequisite: 
1. Install a MQTT server. If running Hassio, highly suggest: https://www.home-assistant.io/addons/mosquitto/
2. Under Hass.io -> "Add-on Store" -> "Add new repository by url" copy/paste: https://github.com/pantomax/hassio-addons

1. Install this addon (it take 5-10 minutes to intall).

2. Copy "rpi-rf_receive.py" to  "/share/rpi-rf_receive.py" share of your hass.io.

3. (optional) Edit "rpi-rf_receive.py" only if you need to change mosquitto address, port, user or password. By default will work without edits if you simply installed official HASSIO Mosquitto Addon with no user/pass/config changes.

4. Start the addon (good idea to view Logs via bottom of addon page for errors)

5. Add this (or similar) code to your hassio configuration.yaml file


```yaml
mqtt:
  broker: core-mosquitto
  discovery: true
  
binary_sensor:
  - platform: mqtt
    state_topic: sensors/rf/receiver
    name: rf1
    payload_on: 4478259
    payload_off: 4478268
```


# Updates/Fixes:
  -  "apparmor": "false" - HASSIO rpi-rf failing to initialize rx due to recent addition of apparmor (fryguy04)
  -  pointing MQTT at "core-mosquitto" instead of static IP. More robust as long as you are using HASSIO's official Mosquitto Addon (fryguy04)
