from spaceship.engine.util import Vec, displayCalc
from spaceship.screen.core import ScreenItem, Screens, style_button, style_keybutton


class Setting(ScreenItem):

    def __init__(self, renderer, data):
        ScreenItem.__init__(self, renderer, data)

        self.back_button = style_button(
            renderer, "Back", displayCalc.percentage(Vec(50, 75)))

        self.key_left = style_keybutton(renderer, self.data.get(
            "key_left", ord('q')), displayCalc.percentage(Vec(30, 10)))
        self.key_right = style_keybutton(renderer, self.data.get(
            "key_right", ord('d')), displayCalc.percentage(Vec(30, 25)))
        
        self.key_up = style_keybutton(renderer, self.data.get(
            "key_up", ord('z')), displayCalc.percentage(Vec(80, 10)))
        self.key_down = style_keybutton(renderer, self.data.get(
            "key_down", ord('s')), displayCalc.percentage(Vec(80, 25)))

        self.key_fire = style_keybutton(renderer, self.data.get(
            "key_fire", ord(' ')), displayCalc.percentage(Vec(50, 40)))
        self.key_pause = style_keybutton(renderer, self.data.get(
            "key_pause", ord('p')), displayCalc.percentage(Vec(50, 55)))

    def label(self, key_button_style, text, margin = 30):
        label_x = self.render.text_size(text, 1)[0]
        self.render.text(text,
                         Vec(key_button_style.position.x - (label_x + margin),
                             key_button_style.position.y + key_button_style.size.y / 2),
                         key_button_style.textSize, key_button_style.textColor)

    def draw(self, input, deltatime):
        ScreenItem.draw(self, input, deltatime)

        self.render.rectangle(Vec.null(), Vec(
            self.render.width, self.render.height), self.data.get("background_color", (0, 0, 0)))

        if self.back_button.draw(input, deltatime):
            return Screens.HOME

        self.label(self.key_pause.current, "Key Pause")
        if self.key_pause.draw(input, deltatime):
            self.data.set("key_pause", self.key_pause.key)

        self.label(self.key_left.current, "Key Left")
        if self.key_left.draw(input, deltatime):
            self.data.set("key_left", self.key_left.key)

        self.label(self.key_right.current, "Key Right")
        if self.key_right.draw(input,deltatime):
            self.data.set("key_right", self.key_right.key)

        self.label(self.key_up.current, "Key Up")
        if self.key_up.draw(input, deltatime):
            self.data.set("key_up", self.key_up.key)

        self.label(self.key_down.current, "Key Down")
        if self.key_down.draw(input, deltatime):
            self.data.set("key_down", self.key_down.key)

        self.label(self.key_fire.current, "Key Fire")
        if self.key_fire.draw(input,deltatime):
            self.data.set("key_fire", self.key_fire.key)
