import re
from const import MAX_NAME_LEN, MAX_MESSAGE_LEN
from logger import log


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        super().__init__(self)
        log(log.ERROR, "InvalidUsage:%s", message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def input_check(name, email, message):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if re.search(pattern, email) is None:
        raise InvalidUsage('invalid email')
    if len(message) > MAX_MESSAGE_LEN:
        raise InvalidUsage('long message')
    if len(name) > MAX_NAME_LEN:
        raise InvalidUsage('long name')
    log(log.DEBUG, 'input parameters verified')
