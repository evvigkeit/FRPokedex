from enum import Enum


class RegError(str, Enum):
    WRONG_PASSWORD = 'Oops, wrong password!'
    # to be continued...