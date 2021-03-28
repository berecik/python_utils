import math
from random import choice
from typing import Sequence, Optional
from dataclasses import dataclass


@dataclass
class Codes(object):

    DEFAULT_CHARS = '23456789abcdefghijkmnrstuvwxyz'
    chars: Sequence = DEFAULT_CHARS
    count: Optional[int] = None

    @property
    def chars_len(self):
        return len(self.chars)

    def __call__(
            self,
            length: Optional[int] = None,
            count: Optional[int] = None
    ):
        if length is None:
            if count is None:
                count = self.count
            length = self.code_len(count)
        return "".join([choice(self.chars) for _ in range(length)])

    def code_len(self, count):
        count = max(count, self.chars_len + 1)
        return int(math.log(count, self.chars_len)) + 1


def get_code(*args, **kwargs):
    if "chars" in kwargs:
        chars = kwargs.pop("chars")
    else:
        chars = Codes.DEFAULT_CHARS.upper()
    codes_generator = Codes(chars=chars)
    return codes_generator(*args, **kwargs)


if __name__ == '__main__':
    codes = set()
    for i in range(len(Codes.DEFAULT_CHARS)):
        while True:
            code = get_code(length=1)
            if code not in codes:
                codes.add(code)
                break
    for code in codes:
        print(code)