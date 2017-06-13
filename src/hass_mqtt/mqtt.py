"""Module for MQTT Client connections with reconnection including wifi"""

from umqtt import robust  # pylint: disable=import-error
from machine import unique_id  # pylint: disable=import-error
from ubinascii import hexlify  # pylint: disable=import-error
from .config import Config
from . import wifi

_CONFIG_FILENAME = 'mqtt.json'
_DEFAULT_CONFIG = {
    "enabled": False,
    "server": "<server ip>",
    "client_id": b"esp8266_%s" % hexlify(unique_id()),
    "port": 0,
    "user": None,
    "password": None,
    "keepalive": 0,
    "ssl": False,
    "ssl_params": {}
}
CONFIG = Config(_CONFIG_FILENAME, _DEFAULT_CONFIG)
ERROR_MSG = \
    "MQTT configuration not enabled yet, please adapt and enable CONFIG"
if not CONFIG.enabled:
    print(ERROR_MSG)


class MQTTClient(robust.MQTTClient):
    """Class representing a robust MQTT Client with reconnection support
    including reconnection of the wifi connection itself if neccesary.
    It also supports an optional connection callback function.
    """
    def __init__(self):
        if CONFIG.enabled:
            super().__init__(CONFIG.client_id, CONFIG.server,
                             CONFIG.port, CONFIG.user, CONFIG.password,
                             CONFIG.keepalive, CONFIG.ssl, CONFIG.ssl_params)

    def is_enabled(self):  # pylint: disable=no-self-use
        """Whether or not this MQTT server is enabled"""
        return CONFIG.enabled

    def connect(self, clean_session=True, callback=None):
        """Connect with the MQTT server, calling callback on success"""
        if self.is_enabled():
            result_code = super().connect(clean_session)
            if callback or not hasattr(self, 'connect_cb'):
                self.connect_cb = callback  # pylint: disable=W0201
            if callable(self.connect_cb):
                self.connect_cb(self, result_code)
            return result_code

    def reconnect(self):
        """Reconnect with the MQTT server after having a wifi connection"""
        if self.is_enabled():
            while 1:
                try:
                    return self.connect(False)
                except OSError as error:
                    self.log(True, error)
                    wifi.wait_for_connection()
                    self.delay(0)  # delay with default number of seconds
