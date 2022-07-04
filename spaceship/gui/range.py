
from spaceship.engine.util import Vec
from spaceship.gui.core import GuiItem, Style


class Range(GuiItem):


    @staticmethod
    def create(renderer, position, size):
        default = Style()
        default.color = (200, 200, 200)
        default.borderColor = (0, 0, 0)
        return Range(renderer, size, position, 0, default)

    def __init__(self, render, size, position, value=0, style=Style()):
        GuiItem.__init__(self, render, style)

        self.value = value
        self.size = size
        self.position = position

    def add(self, v=1):
        self.value += v

    def sub(self, v=1):
        self.value -= v

    def draw(self, input, deltatime):
        GuiItem.draw(self, input, deltatime)
        
        if self.value < 0:
            self.value = 0
        elif self.value > 100:
            self.value = 100

        width = (self.size.x*self.value)/100

        self.render.rectangle(
            self.position, Vec(width, self.size.y), self.current.color)

        self.render.border(self.position,self.size, self.current.borderColor, self.current.borderSize)
