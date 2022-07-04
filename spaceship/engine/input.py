import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ['SDL_VIDEO_CENTERED'] = '1'

import pygame
from pygame import *

class Input:

    CLICK_TIME = 0.0
    DOUBLE_CLICK_INTERVAL = 10
    KEY_TAP_TIME = 0.0
    MOUSE_SIZE = 10

    @staticmethod
    def create(width, height):
        return Input(width, height)

    def __init__(self, width, height):

        self._width = width
        self._height = height
        self._isfocused = True
        self._ishidden = False

        self.clicked = False
        self.double_clicked = False
        self.mouse_press = False
        self.mouse_release = False
        self.valid_interval = False
        self.click_pos = [0, 0]

        self.click_time = 0
        self.interval_time = 0

        self.tapped_keys = []
        self.pressed_keys = []
        self.released_keys = []

        self.recording = False
        self.record_keys = []
        self.record_time = 0

        self.is_adjuste = False
        self.adj_size = [0, 0]

        pygame.event.set_blocked(pygame.MOUSEWHEEL)

    def adjuste(self, width, height):
        self.is_adjuste = True
        self.adj_size = [width, height]

    def adjuste_input(self, input):
        out = [input[0], input[1]]
        if self.is_adjuste:
            out[0] = out[0] * self.adj_size[0] / self._width
            out[1] = out[1] * self.adj_size[1] / self._height
        return out

    def start_record(self):
        if not self.recording:
            self.recording = True
            self.record_keys = []
            self.record_time = 0
            return True
        return False

    def get_record(self):
        return [self.record_keys, self.record_time]

    def stop_record(self):
        self.recording = False

        keys = self.record_keys

        self.record_keys = []
        self.record_time = 0

        return keys

    def mouse_down(self):
        return self.mouse_press

    def mouse_up(self):
        v = self.mouse_release
        self.mouse_release = False
        return v

    def mouse_move(self):
        v = self.mouse_moved
        self.mouse_moved = False
        return v

    def mouse_position(self):
        return self.adjuste_input(mouse.get_pos())

    def click(self):
        v = self.clicked
        self.clicked = False
        return v

    def click_position(self):
        return self.click_pos

    def double_click(self):
        v = self.double_clicked
        self.double_clicked = False
        return v

    def key_tap(self, key):
        for k in self.tapped_keys:
            if k == key:
                self.tapped_keys.remove(k)
                return True
        return False

    def key_down(self, key):
        for k in self.pressed_keys:
            if k[0] == key:
                return True
        return False

    def key_up(self, key):
        for k in self.released_keys:
            if k == key:
                self.released_keys.remove(k)
                return True
        return False

    def is_hover(self, width, height, x, y, mx=-1, my=-1):
        pos = self.mouse_position()
        if mx == -1:
            mx = pos[0]
        if my == -1:
            my = pos[1]

        if x < mx + Input.MOUSE_SIZE and x + width > mx:
            if y < my + Input.MOUSE_SIZE and y + height > my:
                return True
        return False

    def update(self, deltatime):
        if self.interval_time > 0:
            self.interval_time -= deltatime * 100
            if self.interval_time < 0:
                self.interval_time = 0

        if self.recording:
            self.record_time += deltatime * 100

        for evt in event.get():
            if evt.type == pygame.QUIT:
                return False

            

            if evt.type == pygame.WINDOWRESIZED:
                self._width = evt.x
                self._height = evt.y

            if evt.type == pygame.WINDOWFOCUSGAINED:
                self._isfocused = True
            elif evt.type == pygame.WINDOWFOCUSLOST:
                self._isfocused = False

            if evt.type == pygame.WINDOWSHOWN:
                self._ishidden = False
            elif evt.type == pygame.WINDOWHIDDEN:
                self._ishidden = True

            if evt.type == MOUSEMOTION:
                self.mouse_moved = True
            else:
                self.mouse_moved = False

            if evt.type == MOUSEBUTTONDOWN:
                x, y = self.adjuste_input(mouse.get_pos())
                self.click_pos = [x, y]
                self.mouse_release = False
                self.mouse_press = True

                self.click_time += deltatime * 100

                if self.interval_time > 0:
                    self.valid_interval = True
                    self.interval_time = 0

            elif evt.type == MOUSEBUTTONUP:
                self.mouse_release = True

                if self.click_time >= Input.CLICK_TIME:
                    if self.valid_interval:
                        self.double_clicked = True
                        self.valid_interval = False
                    else:
                        self.interval_time = Input.DOUBLE_CLICK_INTERVAL

                    self.clicked = True

                self.mouse_press = False
                self.click_time = 0

            if evt.type == KEYDOWN:
                exists = False
                for key in self.pressed_keys:
                    if key[0] == evt.key:
                        key[1] += deltatime * 100
                        exists = True
                        break
                if not exists:
                    self.pressed_keys.append([evt.key, deltatime * 100])
            elif evt.type == KEYUP:
                if self.recording:
                    self.record_keys.append(evt.key)

                for key in self.pressed_keys:
                    if key[0] == evt.key:
                        self.released_keys.append(evt.key)
                        if key[1] >= Input.KEY_TAP_TIME:
                            self.tapped_keys.append(evt.key)
                        self.pressed_keys.remove(key)
                        break
        return True
