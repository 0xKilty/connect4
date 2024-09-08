from enum import Enum

class Slots(Enum):
    EMPTY = "  "
    RED = "\U0001F534" 
    YELLOW = "\U0001F7E1"

class TextStyling(Enum):
    BOLD = "\033[1m"
    BLUE = "\033[34m"
    RESET = "\033[0m"