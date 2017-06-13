"""Module for providing MQTT access from Home Assistantto to GPIO pins"""

import ujson as json  # pylint: disable=import-error
from . import mqtt
from . import wifi
from . import pins as pinz
from .config import Config

SET = b'set'
SWITCH = b'switch'
LIGHT = b'light'
ON = b'on'
OFF = b'off'

_CONFIG_FILENAME = 'hass_mqtt.json'
_DEFAULT_CONFIG = {
    'prefix': 'homeassistant',
    'command_topic_tail': SET
}
CONFIG = Config(_CONFIG_FILENAME, _DEFAULT_CONFIG)


def _partial(func, *args, **kwargs):
    """TODO: Temporary partial method until functools is available for"""
    def _partial(*more_args, **more_kwargs):
        local_kwargs = kwargs.copy()
        local_kwargs.update(more_kwargs)
        return func(*(args + more_args), **local_kwargs)
    return _partial


class MQTTClient(mqtt.MQTTClient):
    """MQTT Client providing discovery topics for Home Assistant"""

    @staticmethod
    def _on_connect(client, result_code):
        """Callback function which is called when a MQTT connection is
        (re-)established.
        """
        print('Connected with result code %d' % result_code)
        for pin in client.pins.values():
            print(b'setting up MQTT for pin %s' % pin.number)
            client.publish(client.get_state_topic(pin),
                           client.get_state_payload(pin.state), True, 1)
            client.publish(client.get_config_topic(pin),
                           client.get_config_payload(pin), True, 1)
        client.subscribe(client.get_commands_subscription_topic())

    @staticmethod
    def _on_message(client, topic, msg):
        """Callback function which is called when a message arrives on
        subscribed topics.
        """
        print(b'Topic: "%s", Message: "%s"' % (topic, msg))
        parts = topic.split(b'/')
        print(parts)
        print(client.get_prefix())
        print(client.get_command_topic_tail())
        if parts[0] == b'%s' % client.get_prefix() \
                and parts[-1] == b'%s' % client.get_command_topic_tail():
            number = int(parts[-2])
            print(b'  Setting Pin %d to %s' % (number, msg))
            pin = client.pins[number]
            pin.set_state(msg == client.get_state_payload(True))
            # Don't use QOS 1 to prevent looping!
            client.publish(client.get_state_topic(pin),
                           client.get_state_payload(pin.state), True, 0)
        else:
            print(" Topic doesn't comply with homeassistant discovery format")

    def __init__(self, pins):
        super().__init__()
        self.pins = pins
        self.set_callback(_partial(MQTTClient._on_message, self))

    def connect(self, clean_session=True, callback=None):
        super().connect(clean_session, MQTTClient._on_connect)

    def get_commands_subscription_topic(self):  # pylint: disable=no-self-use
        """Returns the one wildcard command topic to subscribe to"""
        return b'%s/+/%s/+/%s' % (CONFIG.prefix, mqtt.CONFIG.client_id,
                                  CONFIG.command_topic_tail)

    def get_topic(self, pin, tail):  # pylint: disable=no-self-use
        """Returns a topic using configurations items and specific to a Pin"""
        return b'%s/%s/%s/%s/%s' % (CONFIG.prefix, pin.type_,
                                    mqtt.CONFIG.client_id, pin.number, tail)

    def get_state_topic(self, pin):
        """Returns a state topic, specific to a Pin"""
        return self.get_topic(pin, 'state')

    def get_state_payload(self, state):  # pylint: disable=no-self-use
        """Returns the payload representing a state"""
        return ON if state else OFF

    def get_config_topic(self, pin):
        """Returns a config topic, specific to a Pin"""
        return self.get_topic(pin, 'config')

    def get_config_payload(self, pin):
        """Returns a config payload, specific to a Pin"""
        payload = {
            'name': pin.name,
            'payload_on': ON,
            'payload_off': OFF,
            'command_topic': self.get_topic(pin, SET)
        }
        return b'%s' % json.dumps(payload)

    def get_prefix(self):  # pylint: disable=no-self-use
        """Returns the prefix used for this client"""
        return CONFIG.prefix

    def get_command_topic_tail(self):  # pylint: disable=no-self-use
        """Returns the command topic's tail for this client"""
        return CONFIG.command_topic_tail


def main():
    """Starts a Home Assistant MQTT Client publishing pin states and
    subscribing to all command topics for this node.
    """
    if wifi.is_enabled() and wifi.wait_for_connection():
        client = MQTTClient(pinz.setup())
        client.connect()
        if client.is_enabled():
            while True:
                client.wait_msg()
