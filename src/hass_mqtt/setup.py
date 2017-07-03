"""Module for interactively setting up the hass_mqtt configuration"""
from . import wifi
from . import mqtt
from . import hass_mqtt
from . import pins
from .setup_utils import ask_confirmation


def setup():
    """Set up a complete configuration for wifi, mqtt and pins"""
    if not wifi.is_enabled() or \
       ask_confirmation('Wifi has already been enabled. Set it up again?'):
        wifi.setup()
    if not mqtt.is_enabled() or \
       ask_confirmation('MQTT has already been enabled. Set it up again?'):
        mqtt.setup()
    hass_mqtt.setup()
    pins.setup()


setup()
