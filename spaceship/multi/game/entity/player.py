import os

from spaceship.engine.graphic import Renderer
from spaceship.engine.util import Direction, Vec, displayCalc
from spaceship.multi.game.entity.bullet import Bullet
from spaceship.multi.game.entity.core import Entity, WorldCoord


class Player(Entity):

    
    LV_1 = 11
    LV_2 = 10
    LV_3 = 9
    LV_4 = 8
    LV_5 = 7
    LV_6 = 6
    LV_7 = 5
    LV_8 = 4
    LV_9 = 3
    LV_10 = 2
    LV_11 = 1
    LV_12 = 0

    @staticmethod
    def create_client(wposition, level, fire_callback, map, render, camera):
        player = Player()
        player.shoot_callback = fire_callback
        player.map = map

        player.position = WorldCoord.convert(wposition, camera.size)

        player.camera = camera
        player.render = render

        player.set_level(level)

        return player

    @staticmethod
    def create_server(id, cposition, level, life, csize):
        player = Player()
        player.id = id

        player.life = life
        player.level = level

        player.position = WorldCoord.format(cposition, csize)

        return player

    @property
    def state(self):
        return {
            'client_size': self.client_size.to_dict(),
            'position': self.position.to_dict(),
            'life': self.life,
            'level': self.level,
            'id': self.id,
            'angle': self.angle
        }

    @state.setter
    def state(self, state):
        self.life = state['life']
        self.level = state['level']
        self.id = state['id']
        self.angle = state['angle']
        
        
        self.position.from_dict(state['position'])
        self.client_size.from_dict(state['client_size'])


    

    def __init__(self):
        Entity.__init__(self)

        self.size = displayCalc.percentage(Vec(20, 20))

        self.acceleration_speed = Vec(4000,  4000)

        self.id = Entity.ID_NOTSET
        self.life = 100
        self.level = 0

        self.address = None
        self.socket = None

        self.keys = {
            "key_left": ord('q'),
            "key_right": ord('d'),
            "key_up": ord('z'),
            "key_down": ord('s'),
            "key_fire": ord(' ')
        }

        self.shoot_timer = 30
        self.shoot_callback = None
        self.map = None

        self.last_direction = Direction.NONE
        self.input_lr = Direction.NONE
        self.angle_speed = 0

    def draw(self, input, deltatime):
        self.reset_acceralation()

        self.input_lr = Direction.NONE

        if self.last_direction != Direction.DOWN:

            if self.shoot_timer != 0:
                self.shoot_timer -= deltatime * 100

            if input.key_down(self.keys["key_left"]):
                self.acceleration.x -= self.acceleration_speed.x

                self.input_lr = Direction.LEFT
                if round(self.angle) < 45:
                    self.angle += 100 * deltatime

            if input.key_down(self.keys["key_right"]):
                self.acceleration.x += self.acceleration_speed.x

                self.input_lr = Direction.RIGHT
                if round(self.angle) > -45:
                    self.angle -= 100 * deltatime

            if input.key_tap(self.keys["key_fire"]) or input.click():
                self.fire()

        else:

            if self.shoot_timer != 0:
                self.shoot_timer -= deltatime * 400

        if input.key_down(self.keys["key_up"]):
            self.acceleration.y -= self.acceleration_speed.y

            if round(self.angle) != 0:

                if self.last_direction == Direction.DOWN:
                    self.angle_speed = 150

                move = self.angle_speed * deltatime

                if self.last_direction == Direction.DOWN or self.input_lr == Direction.NONE:
                    if self.angle > 0:
                        self.angle -= move
                    else:
                        self.angle += move

                if self.angle + move > 0 and self.angle - move < 0:
                    self.last_direction = Direction.UP
                    self.angle = 0
                    self.angle_speed = 50

            elif self.angle == 0 and self.last_direction != Direction.UP:
                self.last_direction = Direction.UP
                self.angle_speed = 50

        if input.key_down(self.keys["key_down"]):
            self.acceleration.y += self.acceleration_speed.y

            self.angle_speed = 150
            self.last_direction = Direction.DOWN

            if round(self.angle) != 180:
                self.angle += self.angle_speed * deltatime
                if self.angle > 180:
                    self.angle = 180

        self.motion(deltatime, self.position)

        if self.position.x <= displayCalc.width:
            self.position.x = displayCalc.width
            
            self.reset_acceralation()
            self.velocity.x = 0
        elif self.position.x >= self.map.max_size.x - displayCalc.width:
            self.position.x = self.map.max_size.x - displayCalc.width
            self.reset_acceralation()
            self.velocity.x = 0
        
        if self.position.y <= displayCalc.height:
            self.position.y = displayCalc.height
            self.reset_acceralation()
            self.velocity.y = 0

            # TODO: reset position to spawn + add xp
        elif self.position.y >= self.map.max_size.y - displayCalc.height:
            self.position.y = self.map.max_size.y - displayCalc.height
            self.reset_acceralation()
            self.velocity.y = 0

            # TODO: kill player


        self.camera.x = -self.position.x + self.camera.origin.x
        self.camera.y = -self.position.y + self.camera.origin.y

        self.render.image_ext(self.sprite, self.camera + self.position, self.size, self.angle)

    def set_keys(self, keys):
        self.keys = keys

    def set_level(self, level):
        spriteIndexStart = 0
        spriteIndexEnd = 12

        self.level = level % spriteIndexEnd

        try:
            ships = os.listdir('./assets/ships')
            for i in range(spriteIndexStart, spriteIndexEnd):
                if self.level == i:
                    self.sprite = Renderer.load_image(
                        './assets/ships/'+ships[i])
                    break

            if self.sprite is None:
                raise Exception("")

        except:
            self.sprite = self.render.image_fill((0, 0, 0), self.size)

    def fire(self):
        if self.shoot_callback is not None and self.shoot_timer <= 0:
            self.shoot_timer = 10

            bullet_size = displayCalc.percentage(Vec(5, 10))
            pos = self.position + Vec((self.size.x - bullet_size.x)/2, -bullet_size.y)

            if self.shoot_callback is not None:
                bullet = Bullet.create_client(pos, self.angle, self.render, self.camera)
                bullet.owner = self.id

                self.shoot_callback(bullet)
