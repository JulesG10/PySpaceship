
from spaceship.engine.util import displayCalc, Vec
from spaceship.screen.core import *

class Home(ScreenItem):

    def __init__(self, renderer, data = ScreenData()):
        ScreenItem.__init__(self, renderer, data)

        self.quit_button = style_button(renderer, "Quit", displayCalc.percentage(Vec(50, 70)))
        self.setting_button = style_button(renderer, "Setting", displayCalc.percentage(Vec(50, 50)))
        self.start_button = style_button(renderer, "Start", displayCalc.percentage(Vec(50, 30)))


    def draw(self, input, deltatime):
        ScreenItem.draw(self, input, deltatime)

        self.render.rectangle(Vec.null(), Vec(
            self.render.width, self.render.height), self.data.get("background_color",(0,0,0)))

        if self.quit_button.draw(input, deltatime):
            return Screens.EXIT

        if self.setting_button.draw(input, deltatime):
            return Screens.SETTING

        if self.start_button.draw(input, deltatime):
            return Screens.GAME

        return None
