"""Module for managing GPIO Pins"""

from machine import Pin, Signal  # pylint: disable=import-error
from .config import Config
from .setup_utils import ask_input, ask_number, ask_confirmation

_CONFIG_FILENAME = 'pins.json'
_DEFAULT_CONFIG = {
    0: {'type': 'light', 'name': 'Extra Light'},
    2: {'type': 'switch', 'name': 'Extra Relay'}
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
    """Interactively sets up Home Assistant's MQTT configuration"""
    succes = False  # until proven otherwise
    temp = dict(CONFIG.current)
    print('Interactive setup of your GPIO Pin configuration')
    while 1:
        print('Currently the following pins are configured:')
        print(' pin type   name')
        print(' -------------------')
        for number, config in temp.items():
            print(' %2d  %6s %s' % (number, config['type'], config['name']))
        command = ask_input('What would you like to do?', ('c', 'r', 'q'))
        if command == 'c':
            number = ask_number(
                "What's the number of the pin you'd like to configure?")
            type_ = ask_input(
                "What's the type of pin %d?" % number, ('switch', 'light'),
                temp[number]['type'] if number in temp.keys() else None)
            name = ask_input(
                "What's the name of pin %d?" % number, None,
                temp[number]['name'] if number in temp.keys() else None)
            temp[number] = {'type': type_, 'name': name}
        elif command == 'r':
            number = ask_number(
                "What's the number of the pin you'd like to remove?")
            if number in temp.keys():
                del temp[number]
        elif command == 'q':
            if ask_confirmation(
                    'Do you want to enable and save these settings?'):
                CONFIG.current = temp
                CONFIG.save()
                succes = True
            break
    return succes


def load():
    """Sets up a dictionary of number -> Pins according to configuration"""
    return {
        pin.number: pin for pin in (GPIOPin(number, p['type'], p['name'])
                                    for number, p in CONFIG.current.items())
    }
