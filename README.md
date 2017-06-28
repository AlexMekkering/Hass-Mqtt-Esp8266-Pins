# Hass-Mqtt-Esp8266-Pins
Collection of configurable [MicroPython](http://micropython.org/) scripts for [ESP8266](https://espressif.com/en/products/hardware/esp8266ex/overview) boards which expose their GPIO pins by using MQTT topics which comply with [Home Assistant's](https://home-assistant.io/) [MQTT discovery](https://home-assistant.io/docs/mqtt/discovery/) protocol (starting with Home Assistant 0.48).

## Installation
Installation of Hass-Mqtt-Esp8266-Pins consists of the following steps:
- Install MicroPython on the ESP8266 board by following https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html
- Copy .py files from the src folder to the ESP8266 board
- Restart the ESP8266 board
- Configure Wifi and MQTT settings and configure the GPIO pins

### Prerequisites
First, you need Python3 and optionally pip to ease installation of esptool and Adafruit MicroPython Tool

For flashing the MicroPython firmware, [esptool](https://github.com/espressif/esptool) can be used. This is also available in [pypi](https://pypi.python.org/pypi/esptool) so can easily be installed with pip.

For copying over files to the ESP8266 board after MicroPython has been installed, the [Adafruit MicroPython Tool](https://github.com/adafruit/ampy)(ampy) can be used. This is also available in [pypi](https://pypi.python.org/pypi/adafruit-ampy) so can easily be installed with pip.

For interacting with the Python Interactive Shell on the ESP8266 board via serial connection, [GNU Screen](https://www.gnu.org/software/screen/) can be used (e.g. execute `screen /dev/ttyUSB0 115200` to interact with your ESP8266 board on /dev/ttyUSB0).

#### Home Assistant configuration
For MQTT Discovery to work, Home Assistant should be configured that way, e.g.:
```yaml
# Example configuration.yaml entry
mqtt:
  discovery: true
  discovery_prefix: homeassistant
```
The `discovery_prefix` is `homeassistant` by default.

#### Installing in a virtual environment with Python 3.6
When you've installed Python 3.6, creating a virtual environment in folder `venv` is as easy as `python3 -m venv venv`.
Activating the virtual environment can then be done with `source venv/bin/activate`.
When activated, esptool and Adafruit MicroPython Tool can be installed with `pip3 install esptool adafruit-ampy`

### Copy .py files from the src folder to the ESP8266 board
If you're using a virtual environment make sure it's activated by `source venv/bin/activate`.

The steps are as follows:
1. If needed create a clone of this Github Repository by using `git clone https://github.com/AlexMekkering/Hass-Mqtt-Esp8266-Pins`.
2. `cd Hass-Mqtt-Esp8266-Pins/src`
3. For i.e. a serial connection to the ESP8266 board on `/dev/ttyUSB0`, execute `ampy -p /dev/ttyUSB0 put hass_mqtt`, followed by `ampy -p /dev/ttyUSB0 put main.py`
4. Restart the ESP8266 board

### Configure Wifi and MQTT settings and configure the GPIO pins
_This part assumes that you've got access to the Python Interactive Shell via e.g. `screen /dev/ttyUSB0 115200`_

#### Configure Wifi
First execute `import hass_mqtt.wifi as wifi`. If you've not configured Wifi yet, you'll get the following output:
```
>>> import hass_mqtt.wifi as wifi
Loaded config from wifi.json
WIFI configuration not enabled yet. Please call setup() first!
>>> 
```

To configure Wifi, execute `wifi.setup('<SSID>', '<password>')`, replacing `<SSID>` by your SSID and `<password>` by your password of course.
To verify and enable your configuration, a connection to your access point is trying to be established.

If the connection was succesfull, the following message will be shown whcih 
means you're ready with this part:
```
>>> wifi.setup('<SSID>', '<password>')
#8 ets_task(4020ed88, 28, 3fff9ea8, 10)
WIFI connection detected within 7425 ms
Persistent wifi settings updated
>>>
```
 
If the connection wasn't succesfull within 30 seconds, the following message appears, meaning you'll have to try again:
```
>>> wifi.setup('<SSID>', '<password>')
#7 ets_task(4020ed88, 28, 3fff9ea8, 10)
No WIFI connection detected within 30022 ms
>>> 
```

#### Configre MQTT
First execute `import hass_mqtt.mqtt as mqtt`. If you've not configured Wifi yet, you'll get the following output:
```
>>> import hass_mqtt.mqtt as mqtt
Loaded config from mqtt.json
MQTT configuration not enabled yet, please adapt and enable CONFIG
>>> 
```

To configure MQTT, you'll have to adapt its current CONFIG attributes. You can check which attributes are available by `print(mqtt.CONFIG.current)`. The default output before configuration is:
`{'ssl_params': {}, 'enabled': False, 'server': '<server ip>', 'port': 0, 'client_id': 'esp8266_c7c5ef00', 'user': None, 'password': None, 'ssl': False, 'keepalive': 0}`

The `client_id` is pre-configured with your machines `unique_id`.
The only mandatory attribute other than that is `server` which must be filled with your MQTT server's ip address. This can be done by e.g.:
`mqtt.CONFIG['server'] = '192.168.0.1'`

You can fill all attributes analog to this so if you need to set the user name for connection, you'll run `mqtt.CONFIG['user'] = '<user>'` etc.

After you're done, you'll need to enable your settings by running `mqtt.CONFIG['enabled'] = True`, followed by `mqtt.CONFIG.save()`

##### Configure Home Assistant specific settings
When you've configured Home Assistant to use a specific `discovery_prefix` other than the default `homeassistant` for MQTT discovery, you'll need to configure that here also.

t.b.c.
