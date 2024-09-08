from enum import Enum

class Slots(Enum):
    EMPTY = "  "
    RED = "\U0001F534" 
    YELLOW = "\U0001F7E1"

class TextStyling(Enum):
    BOLD = "\033[1m"
    BLUE = "\033[34m"
    GREEN = "\033[32m"
    RESET = "\033[0m"
    CLEAR = "\033c"

class Highlight(Enum):
    BLUE = "\033[44m"
    GREEN = "\033[42m"

class Logging(Enum):
    ERROR = "\U000026D4"
    WARNING = "\u26A0\uFE0F"