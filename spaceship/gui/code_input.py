
import copy
from spaceship.engine.util import displayCalc, Vec
from spaceship.gui.core import GuiItem, Style


class CodeInput(GuiItem):

    @staticmethod
    def create(renderer, position):
        default = Style()
        default.size = displayCalc.percentage(Vec(20, 8))
        default.position = position
        default.color = (200, 200, 200)
        default.borderColor = (0, 0, 0)
        default.borderSize = 1
        default.textColor = (0, 0, 0)
        default.textSize = 1
        default.text = ""

        active = copy.copy(default)
        active.color = (180, 180, 180)
        
        return CodeInput(renderer, None, default, active)

    def __init__(self, render, code, style, active):
        GuiItem.__init__(self, render, style)

        self.active = active
        self.default = style
        self.code = code

        self.no_char = '_'

        self.input_mode = False
        self.input_text = "___-___-___-___"

        self.do_reset = False

    def reset(self, input):
        if input == None:
            self.do_reset = True
        else:
            self.current = self.default
            self.input_mode = False
            self.code = None
            self.input_text = ""
            input.stop_record()

    def draw(self, input, deltatime):
        GuiItem.draw(self, input, deltatime)

        if self.do_reset:
            self.reset(input)
            self.do_reset = False

        if not self.input_mode:
            if input.is_hover(self.current.size.x, self.current.size.y, self.current.position.x, self.current.position.y):
                if input.click():
                    mx, my = input.click_position()
                    if input.is_hover(self.current.size.x, self.current.size.y, self.current.position.x, self.current.position.y, mx, my):
                        self.input_mode = True
                        self.current = self.active
        else:
            if not input.start_record():
                text = input.get_record()[0]
                self.input_text = ""

                for char in text:
                    if char >= ord('a') and char <= ord('z'):
                        self.input_text += chr(char)
                    elif char == ord(' '):
                        self.input_text += self.no_char
                    elif char == 8:
                        self.input_text = self.input_text[:-1]
                
                self.input_text = self.input_text[:3] + "-" + self.input_text[3:6] + "-" + self.input_text[6:9] + "-" + self.input_text[9:]
                self.input_text = self.input_text.upper()

                if len(self.input_text) >= 4 * 3 + 3:
                    self.input_text = self.input_text.replace(self.no_char, '')
                    tmp_text = self.input_text
                    self.reset(input)

                    self.input_text = tmp_text
                    self.code = tmp_text
                
                elif self.code != None:
                    self.code = None

            if input.click():
                self.reset(input)


        self.render.rectangle(self.current.position, self.current.size,
                              self.current.color, self.current.borderRadius)
        self.render.border(self.current.position, self.current.size,
                           self.current.borderColor, self.current.borderSize)

        self.render.text(self.input_text,
                         Vec(self.current.position.x + self.current.size.x /
                             2, self.current.position.y + self.current.size.y/2),
                         self.current.textSize,
                         self.current.textColor,
                         True)
        return self.code