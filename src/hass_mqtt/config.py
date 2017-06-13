"""Module for loading and saving persistent configuration settings"""

import ujson as json  # pylint: disable=import-error


class Config(object):
    """Class representing a configuration based on a json file"""

    def __init__(self, filename, default=None):
        self.filename = filename
        self.current = default
        self.load()

    def load(self):
        """Loads the configuration from the json file"""
        try:
            with open(self.filename) as file_:
                loaded = json.loads(file_.read())
        except (OSError, ValueError):
            print("Couldn't load %s" % self.filename)
            self.save()
        else:
            self.current.update(loaded)
            print("Loaded config from %s" % self.filename)

    def save(self):
        """Saves the configuration to the json file"""
        try:
            with open(self.filename, "w") as file_:
                file_.write(json.dumps(self.current))
        except OSError:
            print("Couldn't save %s" % self.filename)

    def __getattr__(self, name):
        """Act as object proxy for the current configuration"""
        return self.current[name]

    def __getitem__(self, name):
        """Act as dictionary proxy for the current configuration"""
        return self.current[name]

    def __setitem__(self, name, value):
        """Act as dictionary proxy for the current configuration"""
        self.current[name] = value
