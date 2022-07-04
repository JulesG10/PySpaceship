import argparse
import time

from spaceship.multi.game.middleware.server import GameServer

from spaceship.screen.core import ScreenData, Screens
from spaceship.screen.gameover import GameOver
from spaceship.screen.home import Home
from spaceship.screen.multiplayer import Multi
from spaceship.screen.client import MultiClient
from spaceship.screen.setting import Setting
from spaceship.screen.solo import Solo
from spaceship.screen.game import Game

from spaceship.engine.core import Window
from spaceship.engine.graphic import Renderer
from spaceship.engine.input import Input
from spaceship.engine.util import Vec, displayCalc


class SpaceShip:

    def __init__(self, args):
        parser = argparse.ArgumentParser()
        parser.add_argument( '--width', type=int,
                            default=800, required=False, help='Window width')
        parser.add_argument('--height', type=int,
                            default=500, required=False, help='Window height')
        parser.add_argument('--fullscreen', type=bool,
                            default=False, required=False, help='Fullscreen')
        parser.add_argument( '--server', type=bool,
                            default=False, required=False, help='Start in server mode')
        parser.add_argument( '--client', type=str,
                            default=False, required=False, help='Connect to server in client mode')
        

        self.args = parser.parse_args()

        self.window = Window()
        self.renderer = Renderer(self.window)
        self.screen = None
        self.screen_data = ScreenData()
        self.next_screen = None

        self.focus_blur = None

    def update(self, input: Input, deltatime):
        if deltatime > 0:
            self.window.set_title(f"Spaceship - FPS: {round(1 / deltatime)}")

        self.next_screen = self.screen.draw(input, deltatime)
        if self.next_screen is not None:
            if self.next_screen == Screens.HOME:
                self.screen = Home(self.renderer, self.screen.data)
            elif self.next_screen == Screens.SETTING:
                self.screen = Setting(self.renderer, self.screen.data)
            elif self.next_screen == Screens.GAME:
                self.screen = Game(self.renderer, self.screen.data)
            elif self.next_screen == Screens.SOLO:
                self.screen = Solo(self.renderer, self.screen.data)
            elif self.next_screen == Screens.MULTI:
                self.screen = Multi(self.renderer, self.screen.data)
            elif self.next_screen == Screens.GAMEOVER:
                self.screen = GameOver(self.renderer, self.screen.data)
            elif self.next_screen == Screens.CLIENT:
                self.screen = MultiClient(self.renderer, self.screen.data)
            elif self.next_screen == Screens.EXIT:
                self.on_exit()

        if not self.window.isfocused and self.focus_blur is not None:
            self.renderer.alpha(self.focus_blur, Vec(0, 0), 150)

    def on_exit(self):
        if hasattr(self.screen, "on_exit"):
            self.screen.on_exit()
        self.window.stop()

    def start(self):
        if self.args.server:
            server = GameServer(True)
            if server.start():
                try:
                    while server.alive():
                        if server.has_error():
                            server.logger.error(server.get_error())
                            server.server.last_error = ""
                except KeyboardInterrupt:
                    server.close()
            return


        self.window.create(self.args.width, self.args.height, 'Spaceship', self.args.fullscreen)
        ship_icon = Renderer.split_image('./assets/spritesheets/ship.png', Vec(16, 24))[0]
        self.window.set_icon(ship_icon)

        displayCalc.width = self.window.width
        displayCalc.height = self.window.height

        self.focus_blur = self.renderer.image_fill(
            (100, 100, 100), displayCalc.percentage(Vec(100, 100)))

        self.screen_data.set("background_color",
                             (50, 50, 50))  # (186, 144, 28)
        if self.args.client:
            self.screen_data.set("code", self.args.client)
            self.screen = MultiClient(self.renderer, self.screen_data)
        else:
            self.screen = Home(self.renderer, self.screen_data)

        return self.window.start(self.update, self.on_exit)
