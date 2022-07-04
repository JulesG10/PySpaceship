import random
from spaceship.engine.graphic import Renderer
from spaceship.engine.util import  AABB, Direction, displayCalc, Vec
from spaceship.entity.bullet import Bullet


class Enemy:

    BIG = 0
    MEDIUM = 1
    SMALL = 2

    def __init__(self,renderer, type):
        self.render = renderer
        self.sprites = []
        self.frame_index = 0
        
        
        self.size = Vec.null()
        self.position = Vec.null()
        self.direction = Direction.RIGHT

        self.alive = True
        self.life = 0
        self.die_damage = 20

        self.shoot_time = 0
        self.shoot_interval = 0
        self.shoot_type = Bullet.LASER

        self.max_x = self.random_range()
        self.min_x = self.random_range()

        if self.max_x < self.min_x:
            self.max_x, self.min_x = self.min_x, self.max_x

        if self.max_x - self.min_x <= 20:
            self.max_x += 20
        

        self.max_x *= 10
        self.min_x *= 10

        if self.max_x + self.size.x > displayCalc.width:
            self.max_x = displayCalc.width - self.size.x
            self.min_x -= self.size.x

        self.type = type
        self.load(type)

    def random_range(self):
        return random.randint(0, displayCalc.width//10)

    def collision(self, player_pos, player_size):
        if AABB(self.position, player_pos, self.size, player_size):
                self.alive = False
                return self.position
        return Vec.null()

    def load(self, type):
        if type == Enemy.BIG:
            self.life = 30
            self.shoot_interval = 150
            self.shoot_type = Bullet.LASER
            self.sprites = Renderer.split_image('./assets/spritesheets/enemy-big.png', Vec(32, 32))
            self.size = displayCalc.percentage(Vec(16, 16))
        elif type == Enemy.MEDIUM:
            self.life = 20
            self.shoot_type = Bullet.BOLTS
            self.shoot_interval = 150
            self.sprites = Renderer.split_image('./assets/spritesheets/enemy-medium.png', Vec(32, 16))
            self.size = displayCalc.percentage(Vec(16, 8))
        else:
            self.life = 10
            self.shoot_interval = 50
            self.shoot_type = Bullet.LASER
            self.sprites = Renderer.split_image('./assets/spritesheets/enemy-small.png', Vec(16, 16))
            self.size=displayCalc.percentage(Vec(8, 8))

        self.shoot_time = self.shoot_interval
        self.position = Vec(self.min_x, -self.size.y * 2)

    def fire(self, margin = 0):
        bullet_width = displayCalc.percentage(Vec(4, 8)).x
        pos = Vec(self.position.x + self.size.x/2 + margin - bullet_width/2,
                  self.position.y + self.size.y)
        return Bullet(self.render, pos, Direction.DOWN, self.shoot_type)

    def draw(self, game, deltatime):
        if self.life <= 0:
            self.alive = False
            return self.position

        self.shoot_time += deltatime * 100
        if game.player.position.y > self.position.y:
            if self.shoot_time >= self.shoot_interval:
                self.shoot_time = 0

                if self.type == Enemy.BIG:
                    game.bullets.append(self.fire(10))
                    game.bullets.append(self.fire(-10))
                else:
                    game.bullets.append(self.fire())

        self.position.y += deltatime*100
        if self.position.y > displayCalc.height + self.size.y:
            self.alive = False
            return self.position

        if self.direction == Direction.LEFT:
            self.position.x -= deltatime*100
            if self.position.x < self.min_x:
                self.direction = Direction.RIGHT
        else:
            self.position.x += deltatime*100
            if self.position.x > self.max_x:
                self.direction = Direction.LEFT

        self.frame_index += deltatime * 10
        index = int(self.frame_index) % len(self.sprites)
        self.render.image_ext(self.sprites[index], self.position, self.size)

        return Vec.null()
