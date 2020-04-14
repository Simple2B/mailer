import pathlib
import json
from invalid_usage import InvalidUsage


PATH_TO_CONF_FILE = str(pathlib.Path(__file__).parent.absolute().joinpath('config.json'))


class Settings(object):
    def __init__(self):
        # Read preferences
        self.conf = None
        with open(PATH_TO_CONF_FILE, 'r') as f:
            self.conf = json.load(f)
        if not self.conf:
            raise InvalidUsage('Bad settings file')
