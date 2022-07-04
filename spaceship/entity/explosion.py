
from re import S
from spaceship.engine.graphic import Renderer
from spaceship.engine.util import Vec, displayCalc


class Explosion:
    EXPLOSION_SPRITES = []

    def __init__(self,render, position):
        self.render = render
        self.position = position
        self.frame_index = 0
        self.speed = 200
        self.alive = True
        self.size = displayCalc.percentage(Vec(8,8))

        if len(Explosion.EXPLOSION_SPRITES) == 0:
            Explosion.EXPLOSION_SPRITES = Renderer.split_image(
                './assets/spritesheets/explosion.png', Vec(16, 16))

    def draw(self, deltatime):
        if self.alive:
            self.position.y += deltatime * self.speed

            index = int(self.frame_index) % len(Explosion.EXPLOSION_SPRITES)
            self.render.image_ext(
                Explosion.EXPLOSION_SPRITES[index], self.position, self.size)

            self.frame_index += deltatime * 10
            if self.frame_index >= len(Explosion.EXPLOSION_SPRITES):
                self.alive = False
        
        return not self.alive
