from gamecontroller import GameController

ROWS = 6
COLUMNS = 7
UNIT = 100
gc = GameController(ROWS, COLUMNS, UNIT)


def setup():
    size(COLUMNS*UNIT, (ROWS+1)*UNIT)


def draw():

    global ROWS
    global COLUMNS
    global UNIT
    GREY = (220, 220, 220)

    background(*GREY)

    gc.drop_disk_in_turns(mouseX, mouseY)
    gc.refresh_frame()


def mouseReleased():
    gc.when_mouse_released(mouseX, mouseY)
