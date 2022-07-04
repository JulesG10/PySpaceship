import random
from spaceship.engine.util import Direction, DisplayCalculations, Vec
from spaceship.engine.graphic import Renderer

class Cloud:

    def __init__(self):
        self.time = 0
        self.position = Vec.null()

        self.opacity_frame = Renderer.load_image('./assets/backgrounds/clouds-transparent.png')
        self.default_frame = Renderer.load_image('./assets/backgrounds/clouds.png')

        self.active = False
        self.size = DisplayCalculations.percentage(Vec(100, 40))
        self.margin = 0
        self.next_time = self._random_time(10,20)

    def _random_time(self, sec1, sec2):
        return random.randint(sec1 * 100, sec2 * 100)

    def background(self, draw, deltatime):

        if not self.active:
            self.time += deltatime * 100
            if self.time >= self.next_time:
                self.next_time = self._random_time(10,20)
                
                # dbg('New cloud, next spawn in {0} seconds'.format(
                #     int(self.next_time/100)), 'GameInfo')

                self.time = 0
                self.active = True

                self.position = Vec(0, -(DisplayCalculations.pixel(Vec(0, 5).x+self.size.x)))
                self.margin = DisplayCalculations.pixel(Vec(0, random.randint(6, 10))).y
        else:
            self.position[0] += deltatime * 80
            self.position[1] += deltatime * 100
            if self.position[0] >= DisplayCalculations.width:
                self.position[0] = 0

            if self.position[1] >= DisplayCalculations.height:
                self.active = False

            draw.effect(self.sprites[1], self.position[0],
                        self.position[1], self.size)
            draw.effect(self.sprites[1], self.position[0]-self.size[0]-1,
                        self.position[1], self.size, 0, 1, (True, False))

    def opacity(self, draw):
        if self.active:
            draw.effect(self.opacity_frame, self.position.x,self.position.y + self.margin, self.size)
            draw.effect(self.opacity_frame, self.position.x-self.size.x-1 ,self.position+self.margin, self.size, 0, 1, (True, False))
