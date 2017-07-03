# Hass-Mqtt-Esp8266-Pins
Collection of (re-)configurable [MicroPython](http://micropython.org/) scripts for [ESP8266](https://espressif.com/en/products/hardware/esp8266ex/overview) boards which expose their GPIO pins by using MQTT topics which comply with [Home Assistant's](https://home-assistant.io/) [MQTT discovery](https://home-assistant.io/docs/mqtt/discovery/) protocol (starting with Home Assistant 0.48).

## Installation
### TL;DR for ESP8266 on /dev/ttyUSB0
Installation of Hass-Mqtt-Esp8266-Pins consists of the following 4 steps:
1. Flash the  MicroPython firmware on the ESP8266 board by following https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html
   ```
   esptool.py --port /dev/ttyUSB0 erase_flash
   esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170612-v1.9.1.bin
   ```
2. Copy .py files from the src folder to the ESP8266 board
   ```
   git clone https://github.com/AlexMekkering/Hass-Mqtt-Esp8266-Pins.git
   ampy -p /dev/ttyUSB0 put Hass-Mqtt-Esp8266-Pins/src/hass_mqtt
   ampy -p /dev/ttyUSB0 put Hass-Mqtt-Esp8266-Pins/src/main.py
   ```
3. Configure Wifi, MQTT and GPIO pin settings
   ```
   screen /dev/ttyUSB0 115200
   
   >>> import hass_mqtt.setup
   ```
   ... and let the interactive setup process guide you ...
4. Restart the ESP8266 board
   `>>> from machine import reset; reset()`

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
