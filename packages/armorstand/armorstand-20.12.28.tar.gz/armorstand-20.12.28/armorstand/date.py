from datetime import datetime
from doctest import testmod
from enum import Enum
from typing import List


class DateCode(Enum):
    SHORT_DAY_NAME = "%a"
    DAY_NAME = "%A"
    DAY = "%-d"
    ZERO_PADDED_DAY = "%-d"
    SHORT_MONTH = "%b"
    MONTH = "%B"
    MONTH_NUMBER = "%-m"
    YEAR = "%Y"
    SHORT_YEAR = "%y"
    COMMA = ","
    SLASH = "/"


def get_date(order: List[DateCode], return_strf=False) -> str:
    """
    TODO: move tests to separate file
    >>> get_date([DateCode.DAY, DateCode.MONTH, DateCode.COMMA, DateCode.YEAR], return_strf=True)
    '%-d %B, %Y'

    >>> get_date([DateCode.MONTH_NUMBER, DateCode.SLASH, DateCode.DAY, DateCode.SLASH, DateCode.SHORT_YEAR], return_strf=True)
    '%-m/%-d/%y'
    """

    now = datetime.now()

    string = ""
    for index, code in enumerate(order):
        try:
            next_code = order[index + 1]
        except:
            next_code = None

        string += code.value

        if next_code not in (DateCode.COMMA, DateCode.SLASH) and code != DateCode.SLASH:
            string += " "

    if return_strf:
        return string.strip()

    return now.strftime(string).strip()


if __name__ == "__main__":
    testmod(name="get_date", verbose=False)
