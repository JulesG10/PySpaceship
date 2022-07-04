import copy
from spaceship.engine.util import displayCalc, Vec
from spaceship.gui.core import Style, GuiItem


class Button(GuiItem):

    @staticmethod
    def create(renderer, text, position):
        default = Style()
        default.size = displayCalc.percentage(Vec(20, 8))
        default.position = position
        default.color = (200, 200, 200)
        default.borderColor = (0, 0, 0)
        default.borderSize = 1
        default.textColor = (0, 0, 0)
        default.textSize = 1
        default.text = text

        hover = copy.copy(default)
        hover.color = (180, 180, 180)

        return Button(renderer, default, hover, default)

    def __init__(self, render, style, hover, active):
        GuiItem.__init__(self, render, style)

        self.style = style
        self.hover = hover
        self.click = active

    def draw(self, input, deltatime):
        GuiItem.draw(self, input, deltatime)

        if input.is_hover(self.current.size.x, self.current.size.y, self.current.position.x, self.current.position.y):

            if input.mouse_down():
                self.current = self.click
            elif input.click():
                mx, my = input.click_position()
                if input.is_hover(self.current.size.x, self.current.size.y, self.current.position.x, self.current.position.y, mx, my):
                    return True
            else:
                self.current = self.hover
        else:
            self.current = self.style

        self.render.rectangle(self.current.position,
                              self.current.size, self.current.color, self.current.borderRadius)

        self.render.border(self.current.position, self.current.size,
                           self.current.borderColor, self.current.borderSize)
        self.render.text(self.current.text,
                         Vec(self.current.position.x + self.current.size.x /
                             2, self.current.position.y + self.current.size.y/2),
                         self.current.textSize,
                         self.current.textColor,
                         True)

        return False
