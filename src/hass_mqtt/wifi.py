"""Module for configurable Wifi (station) interfaces"""

from network import WLAN, STA_IF  # pylint: disable=F0401
from utime import sleep_ms, ticks_ms, ticks_diff  # pylint: disable=F0401
from machine import reset  # pylint: disable=F0401
from .config import Config

_CONFIG_FILENAME = 'wifi.json'
_DEFAULT_CONFIG = {
    'enabled': False,
    'SSID': '<ssid>',
    'password': '<pwd>',
    'connection_timeout_ms': 3600000,
    'connection_delay_ms': 100
}
CONFIG = Config(_CONFIG_FILENAME, _DEFAULT_CONFIG)
NIC = WLAN(STA_IF)
ERROR_MSG = "WIFI configuration not enabled yet. Please call setup() first!"
if not CONFIG.enabled:
    print(ERROR_MSG)


def setup(ssid, password):
    """Sets up a station Wifi configuration for an SSID and password"""
    was_active = NIC.active()
    NIC.active(True)
    NIC.connect(ssid, password)
    if wait_for_connection(30000, 1000):
        CONFIG['SSID'] = ssid
        CONFIG['password'] = password
        CONFIG['enabled'] = True
        CONFIG.save()
        print("Persistent wifi settings updated")
    else:
        NIC.active(was_active)


def is_enabled():
    """Whether or not this Wifi interface is enabled"""
    return CONFIG.enabled


def connect(ssid=CONFIG.SSID,
            password=CONFIG.password,
            timeout=CONFIG.connection_timeout_ms,
            delay=CONFIG.connection_delay_ms):
    """Connect with the configured accesspoint"""
    if not NIC.isconnected():
        if is_enabled():
            print('connecting to network...')
            NIC.active(True)
            NIC.connect(ssid, password)
            if not wait_for_connection(timeout, delay):
                reset()  # as a last resort, reset after connection timeout
            else:
                print('network config: ', NIC.ifconfig())
        else:
            print(ERROR_MSG)
    else:
        print('network already connected')


def wait_for_connection(maximum_duration_ms=CONFIG.connection_timeout_ms,
                        wait_ms=CONFIG.connection_delay_ms):
    """Waits for a connection for maximum_duration_ms, polls every wait_ms"""
    if not NIC.isconnected():
        report_string = "Wifi connection detected within %d ms"
        ticks_start = ticks_ms()
        elapsed_ms = ticks_diff(ticks_ms(), ticks_start)
        while ((not maximum_duration_ms or elapsed_ms < maximum_duration_ms)
               and NIC.active()
               and not NIC.isconnected()):
            print('.', end='', flush=True)
            sleep_ms(wait_ms)
            elapsed_ms = ticks_diff(ticks_ms(), ticks_start)
        print('')
        if NIC.isconnected():
            print(report_string % ticks_diff(ticks_ms(), ticks_start))
        else:
            print("No %s" % (report_string % elapsed_ms))
    else:
        print('Wifi already connected')
    return NIC.isconnected()
