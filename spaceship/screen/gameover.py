from spaceship.engine.util import Vec, displayCalc
from spaceship.screen.core import ScreenItem, Screens, style_button


class GameOver(ScreenItem):

    def __init__(self, renderer, data):
        ScreenItem.__init__(self, renderer, data)
        
        self.color = [0,0,0]
        self.target_color = self.data.get("background_color", (0,0,0))
        
        self.player = self.data.get("player",{"score":0,"kill":0})
        self.back_button = style_button(renderer, "Back", displayCalc.percentage(Vec(50, 75)))
        



    def draw(self, input, deltatime):
        ScreenItem.draw(self, input, deltatime)

        for i in range(0,3):
            if self.color[i] < self.target_color[i]:
                self.color[i] += deltatime * 250
        
        self.render.rectangle(Vec.null(), Vec(self.render.width, self.render.height), self.color)

        self.render.text("Game Over",
            displayCalc.percentage(Vec(50, 20)), 5, (0, 0, 0), True)

        self.render.text("Score " + str(round(self.player["score"],2)),
            displayCalc.percentage(Vec(50, 40)), 2, (0, 0, 0), True)

        if self.player["kill"] > 0:
            self.render.text(str(self.player["kill"]) + " Kill",
                displayCalc.percentage(Vec(50, 50)), 2, (0, 0, 0), True)

        if self.back_button.draw(input, deltatime):
            return Screens.HOME