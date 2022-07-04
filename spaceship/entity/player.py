from spaceship.engine.graphic import Renderer
from spaceship.engine.util import Direction, displayCalc, Vec
from spaceship.entity.bullet import Bullet


class Player:

    def __init__(self, render):
        self.render = render
        self.sprites = Renderer.split_image(
            './assets/spritesheets/ship.png', Vec(16, 24))
        self.frame_index = 0

        self.size = displayCalc.percentage(Vec(8, 12))
        self.position = Vec((displayCalc.width - self.size.x)/2,
                            displayCalc.height - (self.size.y * 2))

        self.velocity = 0
        self.acceleration = 0
        self.friction = -5
        self.acceleration_speed = 4000

        self.shoot_time = 0
        self.shoot_interval = 10

        self.life = 100
        self.kill = 0
        self.score = 0

        self.key_left = 0
        self.key_right = 0
        self.key_fire = 0

    def set_keys(self, key_left, key_right, key_fire):
        self.key_left = key_left
        self.key_right = key_right
        self.key_fire = key_fire

    def add_kill(self):
        self.kill += 1
        self.score += 100

    def draw(self, game, input, deltatime):
        self.shoot_time -= deltatime * 100
        if self.shoot_time <= 0:
            self.shoot_time = 0

        self.frame_index += deltatime * 10
        # x = self.position.x + self.velocity * deltatime
        # if x >= 0 and x <= displayCalc.width - self.size.x:
        #     self.position.x = x

        # self.velocity *= 0.9
        # if self.velocity < 0.1 and self.velocity > -0.1:
        #     self.velocity = 0

        
        image = self.sprites[int(self.frame_index) % len(self.sprites)]
        self.render.image_ext(image, self.position, self.size)

        if input.key_tap(self.key_fire) or input.click():
            bullet = self.fire()
            if bullet:
                game.bullets.append(bullet)


        self.acceleration = 0
        if input.key_down(self.key_left):
            self.move_left(deltatime)

        if input.key_down(self.key_right):
            self.move_right(deltatime)

        self.acceleration += self.velocity * self.friction
        self.velocity += self.acceleration * deltatime
        self.position.x += (self.velocity * deltatime) + (self.acceleration * 0.5) * (deltatime ** 2)
        

        if self.position.x > displayCalc.width - self.size.x:
            self.position.x = displayCalc.width - self.size.x
            self.velocity = 0

        if self.position.x < 0:
            self.position.x = 0
            self.velocity = 0

        if self.life <= 0:
            return self.position

        return Vec.null()

    def move_left(self, deltatime):
        # self.velocity -= 25
        self.acceleration -= self.acceleration_speed

    def move_right(self, deltatime):
        # self.velocity += 25
        self.acceleration += self.acceleration_speed

    def fire(self):
        if self.shoot_time <= 0:
            self.shoot_time = self.shoot_interval

            bullet_width = displayCalc.percentage(Vec(4, 8)).x
            pos = Vec(self.position.x + bullet_width / 2,
                      self.position.y - self.size.y)

            return Bullet(self.render, pos, Direction.UP, Bullet.LASER)
