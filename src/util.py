from enum import Enum

def pause(s=""):
    x = input("{}\nAny key to quit, <ENTER> to continue: ".format(s))
    return x == ""


class RoomType(Enum):
    LOUNGE = 'LOUNGE'
    RESTAURANT = 'RESTAURANT'
    DINING = 'DINING'
