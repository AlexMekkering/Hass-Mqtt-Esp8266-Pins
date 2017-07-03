"""Module for MQTT Client connections with reconnection including wifi"""

from umqtt import robust  # pylint: disable=import-error
from machine import unique_id  # pylint: disable=import-error
from ubinascii import hexlify  # pylint: disable=import-error
from .config import Config
from . import wifi
from .setup_utils import ask_input, ask_number, ask_confirmation, ask_dict


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


def setup():
    """Interactively sets up the basic MQTT configuration"""
    succes = False  # until proven otherwise
    print('Interactive setup of your MQTT connection:')
    print('  Current status: %s' % 'enabled' if is_enabled() else 'disabled')
    temp = {}
    temp['server'] = ask_input(' server', None,
                               CONFIG.server if is_enabled() else None)
    temp['port'] = ask_number(' port', 0)
    temp['client_id'] = ask_input(' client id', None, CONFIG.client_id)
    if ask_confirmation(' Set user and password?', False):
        temp['user'] = ask_input('  user', None, CONFIG.user)
        temp['password'] = ask_input('  password')
    temp['keepalive'] = ask_number(' keepalive', CONFIG.keepalive)
    temp['ssl_params'] = ask_dict(' ssl params', CONFIG.ssl_params)
    temp['ssl'] = temp['ssl_params'] != {}
    if ask_confirmation(
            'Are you sure you want to enable and save these settings?'):
        CONFIG.current.update(temp)
        CONFIG['enabled'] = True
        CONFIG.save()
        succes = True
    return succes


def is_enabled():
    """Whether or not the MQTT client is enabled"""
    return CONFIG.enabled


class MQTTClient(robust.MQTTClient):
    """Class representing a robust MQTT Client with reconnection support
    including reconnection of the wifi connection itself if neccesary.
    It also supports an optional connection callback function.
    """
    def __init__(self):
        if is_enabled():
            super().__init__(CONFIG.client_id, CONFIG.server,
                             CONFIG.port, CONFIG.user, CONFIG.password,
                             CONFIG.keepalive, CONFIG.ssl, CONFIG.ssl_params)

    def connect(self, clean_session=True, callback=None):
        """Connect with the MQTT server, calling callback on success"""
        if is_enabled():
            result_code = super().connect(clean_session)
            if callback or not hasattr(self, 'connect_cb'):
                self.connect_cb = callback  # pylint: disable=W0201
            if callable(self.connect_cb):
                self.connect_cb(self, result_code)
            return result_code

    def reconnect(self):
        """Reconnect with the MQTT server after having a wifi connection"""
        if is_enabled():
            while 1:
                try:
                    return self.connect(False)
                except OSError as error:
                    self.log(True, error)
                    wifi.wait_for_connection()
                    self.delay(0)  # delay with default number of seconds
