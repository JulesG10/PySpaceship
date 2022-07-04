import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ['SDL_VIDEO_CENTERED'] = '1'

import time
import pygame
from pygame import display
from pygame.constants import *
from spaceship.engine.input import Input

class Window:

    def __init__(self):
        pygame.init()

        self.width = 0
        self.height = 0
        self.title = ''
        self.isfocused = True
        self.ishidden = False

        self.active = False
        self.initialized = False

        self.renderer = None
        self.input = None

        self.fullscreen = False
        self.fullscreen_render = None
        self.fullscreen_mode = (0,0)

    def set_title(self, title):
        display.set_caption(title)
        self.title = title

    def set_icon(self, icon):
        if type(icon) == str and os.path.exists(icon):
            surf = pygame.image.load(icon)
            display.set_icon(surf)
        elif type(icon) == pygame.Surface:
            display.set_icon(icon)

    def create(self, width=800, height=500, title='', fullscreen=False, resize=False, input_processor=Input):
        self.width = width
        self.height = height
        self.title = title

        self.active = True
        self.initialized = True

        
        self.fullscreen = fullscreen
        if self.fullscreen:
            modes = display.list_modes()
            if len(modes) > 0:
                self.fullscreen_mode = modes[0]
            else:
                self.fullscreen_mode = (width, height)

            self.fullscreen_render = display.set_mode(self.fullscreen_mode, FULLSCREEN | DOUBLEBUF | HWSURFACE)
            self.renderer = pygame.Surface((width, height))

            self.input = input_processor(self.fullscreen_mode[0], self.fullscreen_mode[1])
            self.input.adjuste(width, height)
        else:
            attr = HWSURFACE | DOUBLEBUF
            if resize:
                attr = HWSURFACE | DOUBLEBUF | RESIZABLE

            self.renderer = display.set_mode(
                (self.width, self.height), attr)

            self.input = input_processor.create(width, height)
        display.set_caption(self.title)

    def stop(self):
        self.active = False

    def start(self, game, on_exit = None):
        if not self.initialized:
            return 1
        
        if not game:
            return 1

        self.active = True

        last_time = 0
        current_time = 0

        while self.active:

            current_time = float(time.time())
            deltatime = (current_time - last_time)
            last_time = current_time

            self.renderer.fill((0, 0, 0))
            self.active = self.input.update(deltatime)
            if on_exit is not None and not self.active:
                on_exit()
                


            self.isfocused = self.input._isfocused
            self.ishidden = self.input._ishidden
            self.width = self.input._width
            self.height = self.input._height

            game(self.input, deltatime)

            if self.fullscreen:
                self.fullscreen_render.blit(pygame.transform.scale(self.renderer, self.fullscreen_mode), (0,0))

            display.flip()
        pygame.quit()
        return 0
