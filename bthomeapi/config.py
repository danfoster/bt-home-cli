import yaml
import os
import pathlib
import logging
import sys


logger = logging.getLogger(__name__)

class Config:

    def __init__(self):
        self.filename = os.path.expanduser("~/.config/bthome/bthome.yml")
        self.load(self.filename)
        self.set_defaults()
        
    def __del__(self):
        self.save(self.filename)

    def load(self, filename):
        """
        Loads the configration from disk
        """

        if not os.path.exists(filename):
            dirname = os.path.dirname(filename)
            pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
            pathlib.Path(filename).touch()
            self.config = {}
        
        with open(filename) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader) or {}

    def save(self, filename):
        """
        Saves the configuration to disk
        """
        if not os.path.exists(filename):
            dirname = os.path.dirname(filename)
            pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)

        with open(filename, 'w') as file:
            yaml.dump(self.config, file)


    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        self.config[key] = value

   

    def set_defaults(self):
        pass

    def validate(self):
        """
        Checks the current config is valid and sets any sensible defaults
        """
        pass