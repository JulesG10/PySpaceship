import random
from spaceship.engine.util import AABB, Direction, displayCalc, Vec
from spaceship.engine.graphic import Renderer



class Bullet:
    LASER = 0
    BOLTS = 1

    LASER_SPRITES = []
    BOLT_SPRITES = []

    def __init__(self, render, position, direction, type):
        self.position = position
        self.direction = direction
        self.size = displayCalc.percentage(Vec(4, 8))

        self.alive = True

        self.frame_index = 0
        self.render = render
        self.type = type

        self.speed = 800
        self.bolts = []
        self.damage = 5

        if type == Bullet.BOLTS:
            self.size = displayCalc.percentage(Vec(4, 4))
            self.speed = 200
            self.damage = 2

            for i in range(random.randint(5, 10)):
                space = displayCalc.percentage(
                    Vec(random.randint(10, 20), random.randint(0, 4)))
                self.bolts.append(Vec(self.position.x + space.x, self.position.y + space.y))

        if len(Bullet.LASER_SPRITES) == 0 or len(Bullet.BOLT_SPRITES) == 0:
            sprites = Renderer.split_image(
                './assets/spritesheets/laser-bolts.png', Vec(16, 16))

            Bullet.LASER_SPRITES = sprites[2:]
            Bullet.BOLT_SPRITES = sprites[:2]

    def collision(self, position, size):
        if self.type == Bullet.LASER:
            if AABB(self.position, position, self.size, size):
                self.alive = False
                return True
            return False
        else:
            hit = False
            for bolt in self.bolts:
                if AABB(bolt, position, self.size, size):
                    self.bolts.remove(bolt)
                    hit = True
            self.alive = len(self.bolts) > 0
            return hit

    def draw(self, deltatime):
        self.frame_index += deltatime * 10
        
        if self.type == Bullet.LASER:
            if self.direction == Direction.UP:
                self.position.y -= self.speed * deltatime
            else:
                self.position.y += self.speed * deltatime

            if self.position.y < 0 or self.position.y > displayCalc.height:
                self.alive = False

            index = int(self.frame_index) % len(Bullet.LASER_SPRITES)
            self.render.image_ext(Bullet.LASER_SPRITES[index], self.position, self.size,
                          0, 1, (False, self.direction != Direction.UP))

        else:

            if self.position.y < 0 or self.position.y > displayCalc.height:
                self.alive = False

            index = int(self.frame_index) % len(Bullet.BOLT_SPRITES)

            for bolt in self.bolts:

                if random.randint(0, 1):
                    bolt.x += self.speed * 2 * deltatime
                else:
                    bolt.x -= self.speed * 2 * deltatime

                if self.direction == Direction.UP:
                    bolt.y -= self.speed * deltatime
                else:
                    bolt.y += self.speed * deltatime

                self.render.image_ext(Bullet.BOLT_SPRITES[index], bolt, self.size)
                
                if bolt.y < 0 or bolt.y > displayCalc.height:
                    self.bolts.remove(bolt)

            if len(self.bolts) == 0:
                self.alive = False

        return self.alive



