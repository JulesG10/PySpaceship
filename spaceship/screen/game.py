from spaceship.engine.util import Vec, displayCalc
from spaceship.screen.core import ScreenItem, Screens, style_button


class Game(ScreenItem):

    def __init__(self, renderer, data):
        ScreenItem.__init__(self, renderer, data)

        self.solo_button = style_button(renderer, "Solo", displayCalc.percentage(Vec(50, 30)))
        self.multi_button = style_button(renderer, "Multiplayer (beta)", displayCalc.percentage(Vec(50, 50)))
        self.back_button = style_button(renderer, "Back", displayCalc.percentage(Vec(50, 70)))

    def draw(self, input, deltatime):
        ScreenItem.draw(self, input, deltatime)

        self.render.rectangle(Vec.null(), Vec(
            self.render.width, self.render.height), self.data.get("background_color", (0, 0, 0)))

        if self.solo_button.draw(input, deltatime):
            return Screens.SOLO

        if self.multi_button.draw(input, deltatime):
            return Screens.MULTI

        if self.back_button.draw(input, deltatime):
            return Screens.HOME
