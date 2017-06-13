"""Module for managing GPIO Pins"""

from machine import Pin, Signal  # pylint: disable=import-error
from .config import Config

_CONFIG_FILENAME = 'pins.json'
_DEFAULT_CONFIG = {
    'pins': ({'number': 0, 'type': 'light', 'name': 'Extra Light'},
             {'number': 2, 'type': 'switch', 'name': 'Extra Relay'})
}
CONFIG = Config(_CONFIG_FILENAME, _DEFAULT_CONFIG)


class GPIOPin(object):  # pylint: disable=too-few-public-methods
    """Represents a GPIO Pin(number) on the board,
    assigns a name and defines it as of a specific kind.
    """
    def __init__(self, number, type_, name):
        self.number = number
        self.type_ = type_
        self.name = name
        self.pin = Signal(number, Pin.OUT, invert=number < 15)
        self.set_state(False)

    def set_state(self, state):
        """Sets the state of the pin to on (True) or off (False)"""
        self.state = state
        if state:
            self.pin.on()
        else:
            self.pin.off()


def setup():
    """Sets up a dictionary of number -> Pins according to configuration"""
    return {
        pin.number: pin for pin in (GPIOPin(p['number'], p['type'], p['name'])
                                    for p in CONFIG.pins)
    }
