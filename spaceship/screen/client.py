from spaceship.engine.util import displayCalc, Vec
from spaceship.multi.game.middleware.client import GameClient
from spaceship.multi.game.world.world import World
from spaceship.multi.tcp.util import decode_ip
from spaceship.screen.core import *


class MultiClient(ScreenItem):

    def __init__(self, renderer, data=ScreenData()):
        ScreenItem.__init__(self, renderer, data)

        self.code = self.data.get("code", None)
        self.data.set("code", None)
        ip = decode_ip(self.code.lower())

        self.client = GameClient(ip)
        
        self.pause = False

        self.back_button = style_button(
            renderer, "Back", displayCalc.percentage(Vec(50, 70)))
        self.exit_game = style_button(
            renderer, "Exit Game", displayCalc.percentage(Vec(50, 50)))
        self.play_button = style_button(renderer, "Play", displayCalc.percentage(Vec(50, 30)))

        self.blur = self.render.image_fill(
            (100, 100, 100), displayCalc.percentage(Vec(100, 100)))

        self.data.get("key_left", ord('q'))
        self.data.get("key_right", ord('d'))
        self.data.get("key_up", ord('z'))
        self.data.get("key_down", ord('s'))
        self.data.get("key_fire", ord(' '))
        self.data.get("key_pause", ord('p'))

        self.world = World(self.render, self.client, self.data)
        

    def on_exit(self):
        self.client.close()

    def label(self, text, position, color=(255, 255, 255), center=False):
        return self.render.text(text, position, 1, color, center)

    def draw(self, input, deltatime):
        ScreenItem.draw(self, input, deltatime)
        if self.code == None:
            return Screens.MULTI

        if self.client.wait_for_connect == GameClient.WAIT:
            self.render.rectangle(Vec.null(), Vec(
                self.render.width, self.render.height), self.data.get("background_color", (0, 0, 0)))
            
            self.label("Connecting...", displayCalc.percentage(Vec(50, 40)), (255, 255, 255), True)
        elif self.client.has_error() or self.client.wait_for_connect == GameClient.ERROR:
            self.render.rectangle(Vec.null(), Vec(
                self.render.width, self.render.height), self.data.get("background_color", (0, 0, 0)))

            spaces = self.client.get_error().split(' ')

            start_part = " ".join(spaces[: len(spaces) // 2])
            end_part = " ".join(spaces[len(spaces) // 2:])
            self.label(start_part, displayCalc.percentage(Vec(50, 30)), (200, 10, 10), True)
            self.label(end_part, displayCalc.percentage(Vec(50, 35)), (200, 10, 10), True)

            if self.back_button.draw(input, deltatime):
                self.client.close()
                return Screens.HOME            
        elif self.client.wait_for_connect == GameClient.RUN:
            if input.key_tap(self.data.get("key_pause")):
                self.pause = not self.pause
                
                if self.pause:
                    self.client.pause()
                else:
                    self.client.resume()

            if self.pause:
                self.render.alpha(self.blur, Vec(0, 0), 200)
                
                if self.exit_game.draw(input, deltatime):
                    self.client.close()
                    return Screens.HOME
                
                if self.play_button.draw(input, deltatime):
                    self.pause = False
                    self.client.resume()
            else:
                self.world.draw(input, deltatime)
        else:
            self.label("Connection error", displayCalc.percentage(Vec(50, 30)), (200, 10, 10), True)
            if self.back_button.draw(input, deltatime):
                self.client.close()
                return Screens.HOME

        return None
