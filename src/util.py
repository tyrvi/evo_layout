from enum import Enum
import matplotlib.patches as patches


def pause(s=""):
    x = input("{}\nAny key to quit, <ENTER> to continue: ".format(s))
    return x == ""


class RoomTypes(Enum):
    LOUNGE = 'LOUNGE'
    KITCHEN = 'KITCHEN'
    SHOP = 'SHOP'
    DINING = 'DINING'


ROOM_COLORS = {RoomTypes.LOUNGE: 'green',
               RoomTypes.KITCHEN: 'blue',
               RoomTypes.SHOP: 'red',
               RoomTypes.DINING: 'purple'}


def create_color_legend_handles():
    return [patches.Patch(color=ROOM_COLORS[rt], label=rt.value, alpha=0.4) for rt in list(RoomTypes)]
