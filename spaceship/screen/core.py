import copy
from spaceship.engine.graphic import Renderer
from spaceship.gui.code_input import CodeInput
from spaceship.gui.core import Style
from spaceship.engine.util import Vec, displayCalc
from spaceship.gui.button import Button
from spaceship.gui.key_button import KeyButton

class ScreenData:

    def __init__(self, data={}):
        self.data = data

    def get(self, id, no_value=None):
        value = self.data.get(id, None)
        if value == None:
            self.data[id] = no_value
            return no_value
        return value

    def set(self, id, value):
        self.data[id] = value

    def remove(self, id):
        del self.data[id]

    def __str__(self):
        return str(self.data)
        


class ScreenItem:
    
    def __init__(self, renderer: Renderer, data=ScreenData()):
        self.render = renderer
        self.data = data

    def draw(self, input, deltaTime):
        pass


class Screens:
    EXIT = -1
    HOME = 0
    SETTING = 1
    GAME = 2
    GAMEOVER = 4
    SOLO = 5
    MULTI = 6
    CLIENT = 7


def style_codeinput(render, position):
    default = Style()
    default.size = displayCalc.percentage(Vec(30, 12))
    default.position = position - default.size / 2
    default.color = (196, 196, 196)
    default.borderColor = (0, 0, 0)
    default.borderSize = 0
    default.textColor = (0, 0, 0)
    default.textSize = 1
    default.borderRadius = 10
    default.text = ""

    active = copy.copy(default)
    active.borderSize = 2
    active.borderColor = (110, 110, 110)

    return CodeInput(render, None, default, active)

def style_keybutton(render, key, position):
    default = Style()
    default.size = displayCalc.percentage(Vec(12, 12))
    default.position = position - default.size / 2
    default.color = (196, 196, 196)
    default.borderColor = (0, 0, 0)
    default.borderSize = 0
    default.textColor = (0, 0, 0)
    default.textSize = 1
    default.borderRadius = 10
    default.text = key

    active = copy.copy(default)
    active.borderSize = 2
    active.borderColor = (110, 110, 110)

    return KeyButton(render, key, default, active)

def style_button(render, text, position):
    default = Style()
    default.size = displayCalc.percentage(Vec(30, 12))
    default.position = position - default.size / 2
    default.color = (196, 196, 196)
    default.borderColor = (0, 0, 0)
    default.borderSize = 0
    default.textColor = (0, 0, 0)
    default.textSize = 1
    default.borderRadius = 10
    default.text = text

    hover = copy.copy(default)
    hover.color = (180, 180, 180)

    active = copy.copy(default)
    active.borderSize = 2
    active.borderColor = (110, 110, 110)

    return Button(render, default, hover, active)
