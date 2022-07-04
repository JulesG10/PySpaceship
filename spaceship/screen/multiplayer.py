import time
from spaceship.engine.util import Vec, displayCalc
from spaceship.multi.game.middleware.server import GameServer
from spaceship.screen.core import ScreenItem, Screens, style_button, style_codeinput


class Multi(ScreenItem):
    NONE = 0
    SERVER = 1
    CLIENT = 2

    ACTIVE = 1
    INACTIVE = 0

    def __init__(self, renderer, data):
        ScreenItem.__init__(self, renderer, data)

        self.client_button = style_button(
            renderer, "Client", displayCalc.percentage(Vec(50, 30)))
        self.back_button = style_button(
            renderer, "Back", displayCalc.percentage(Vec(50, 70)))

        self.server_button = style_button(
            renderer, "Server", displayCalc.percentage(Vec(50, 50)))
        self.stop_button = style_button(
            renderer, "Stop", displayCalc.percentage(Vec(50, 50)))
        self.start_button = style_button(
            renderer, "Start", displayCalc.percentage(Vec(50, 50)))

        self.code_input = style_codeinput(
            renderer, displayCalc.percentage(Vec(50, 30)))

        self.mode = Multi.NONE
        self.server_mode = Multi.INACTIVE

        self.multi_server = GameServer()


    def label(self, text, position, color=(255, 255, 255), center=False):
        return self.render.text(text, position, 1, color, center)


    def draw_server(self, input, deltatime):
        if self.multi_server.has_error():
            spaces = self.multi_server.get_error().split(' ')
            start_part = " ".join(spaces[: len(spaces) // 2])
            end_part = " ".join(spaces[len(spaces) // 2:])
            self.label(start_part, displayCalc.percentage(
                Vec(50, 30)), (200, 10, 10), True)
            self.label(end_part, displayCalc.percentage(
                Vec(50, 35)), (200, 10, 10), True)

        else:
            label_size = self.label("Server {0}".format("Active" if self.server_mode == Multi.ACTIVE else "Inactive"),
                                    displayCalc.percentage(Vec(40, 10)))

            circle_position = displayCalc.percentage(Vec(40, 10))
            radius = 6
            margin = 30
            circle_position.x += label_size[0] + radius*2 + margin
            circle_position.y += label_size[1]/2

            if self.server_mode == Multi.ACTIVE:
                self.render.circle(circle_position, radius, (0, 255, 0))
            else:
                self.render.circle(circle_position, radius, (255, 0, 0))

            if self.server_mode == Multi.ACTIVE:
                self.label("Clients: {}".format(self.multi_server.count_clients()), displayCalc.percentage(Vec(40, 20)))
                self.label("Connexion Code: {}".format(self.multi_server.get_code()), displayCalc.percentage(Vec(40, 30)))
                
                if self.stop_button.draw(input, deltatime):
                    self.server_mode = Multi.INACTIVE
                    self.multi_server.close()

            else:
                if self.start_button.draw(input, deltatime):
                    self.server_mode = Multi.ACTIVE
                    if not self.multi_server.start():
                        self.server_mode = Multi.INACTIVE
                        self.multi_server.close()

    def draw(self, input, deltatime):
        ScreenItem.draw(self, input, deltatime)

        self.render.rectangle(Vec.null(), Vec(
            self.render.width, self.render.height), self.data.get("background_color", (0, 0, 0)))

        if self.mode == Multi.NONE:
            if self.client_button.draw(input, deltatime):
                self.mode = Multi.CLIENT

            if self.server_button.draw(input, deltatime):
                self.mode = Multi.SERVER

        elif self.mode == Multi.CLIENT:
            code = self.code_input.draw(input, deltatime)
            if code != None and self.start_button.draw(input, deltatime):
                self.data.set("code", code)
                return Screens.CLIENT

        elif self.mode == Multi.SERVER:
            self.draw_server(input, deltatime)

        if self.server_mode == Multi.INACTIVE and self.back_button.draw(input, deltatime):
            if self.mode != Multi.NONE:
                self.server_mode = Multi.INACTIVE
                self.mode = Multi.NONE
                self.code_input.reset(None)
                self.multi_server.reset()
                return
            return Screens.GAME

    def on_exit(self):
        if self.multi_server.alive():
            self.multi_server.close()
