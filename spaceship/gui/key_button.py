

import copy
from spaceship.engine.util import displayCalc, Vec
from spaceship.gui.core import GuiItem, Style


class KeyButton(GuiItem):

    @staticmethod
    def create(renderer, key, position):
        default = Style()
        default.size = displayCalc.percentage(Vec(8, 8))
        default.position = position

        default.color = (200, 200, 200)
        default.borderColor = (0, 0, 0)
        default.borderSize = 1
        default.textColor = (0, 0, 0)
        default.textSize = 1
        default.text = key

        active = copy.copy(default)
        active.color = (180, 180, 180)

        return KeyButton(renderer, ord(key), default, active)

    def __init__(self, render, keyChar, default, active):
        GuiItem.__init__(self, render, default)

        self.key = keyChar

        self.active = False

        self.default = default
        self.style_active = active

    def draw(self, input, deltatime):
        GuiItem.draw(self, input, deltatime)

        if not self.active:
            if input.is_hover(self.current.size.x, self.current.size.y, self.current.position.x, self.current.position.y):
                if input.click():

                    mx, my = input.click_position()
                    if input.is_hover(self.current.size.x, self.current.size.y, self.current.position.x, self.current.position.y, mx, my):
                        self.active = True
                        self.current = self.style_active
        else:
            if input.click():
                input.stop_record()
                self.active = False
                self.current = self.default

            if not input.start_record():
                if len(input.get_record()[0]) > 0:
                    key = input.stop_record()[0]

                    if (key >= ord('a') and key <= ord('z')) or key == ord(' '):
                        self.key = key
                        self.active = False
                        self.current = self.default

                        return self.key

        self.render.rectangle(self.current.position,
                              self.current.size,
                              self.current.color, self.current.borderRadius)

        self.render.border(self.current.position,
                           self.current.size,
                           self.current.borderColor,
                           self.current.borderSize)

        key_value = chr(self.key).upper()
        if self.key == ord(' '):
            key_value = 'SPACE'
            
        self.render.text(key_value, Vec(self.current.position.x + self.current.size.x / 2,
                         self.current.position.y + self.current.size.y/2), self.current.textSize, self.current.textColor, True)

        return None
