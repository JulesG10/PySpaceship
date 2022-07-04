
from spaceship.engine.util import Vec


class Style:
    def __init__(self):
        self.color = (255, 255, 255)
        self.textColor = (255, 255, 255)
        self.borderColor = (255, 255, 255)

        self.borderSize = 1
        self.textSize = 1
        self.borderRadius = 0
        self.size = Vec.null()
        self.position = Vec.null()
        self.text = ""


class GuiItem:

    def __init__(self,renderer, style = Style()):
        self.current = style
        self.render = renderer

    def draw(self, input, deltatime):
        pass