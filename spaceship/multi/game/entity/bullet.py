from socket import create_server
from venv import create
from spaceship.engine.graphic import Renderer
from spaceship.engine.util import Vec, displayCalc
from spaceship.multi.game.entity.core import Entity, WorldCoord



class Bullet(Entity):

    @property
    def state(self):
        return {
            'position': self.position.to_dict(),
            'angle': self.angle,
            'timer': self.acceleration_timer,
            'speed':self.acceleration_speed.to_dict(),
            'client_size': self.client_size.to_dict(),
            'id': self.id,
            'owner': self.owner
        }

    @state.setter
    def state(self, state):
        self.angle = state['angle']
        self.acceleration_timer = state['timer']
        self.owner = state['owner']
        self.id = state['id']
        
        self.acceleration_speed.from_dict(state['speed'])
        self.client_size.from_dict(state['client_size'])
        self.position.from_dict(state['position'])


    @staticmethod
    def create_server(id, owner, cposition, csize):
        bullet = Bullet()
        bullet.id = id
        bullet.owner = owner

        bullet.position = WorldCoord.format(cposition, csize)

        return bullet

    @staticmethod
    def create_client(wposition, angle, renderer, camera):
        bullet = Bullet()

        bullet.render = renderer
        bullet.camera = camera

        bullet.position = WorldCoord.convert(wposition, WorldCoord.SIZE)
        bullet.angle = -angle

        bullet.set_speed(bullet.angle)

        bullet.sprite = Renderer.load_image("./assets/tiles/tile_0000.png")

        return bullet

    def __init__(self):
        Entity.__init__(self)

        self.size = displayCalc.percentage(Vec(5, 10))
        self.acceleration_timer = 100

        self.acceleration_speed = Vec.null()
        
        self.acceleration_speed.from_angle(self.angle - 90)
        self.acceleration_speed *= 10000

        self.id = Entity.ID_NOTSET
        self.owner = None


    def set_speed(self, angle):
        self.acceleration_speed.from_angle(angle - 90)
        self.acceleration_speed *= 10000

    def draw(self, input, deltatime):
        self.reset_acceralation()

        if self.acceleration_timer > 0:
            self.acceleration_timer -= deltatime * 100
            self.acceleration += self.acceleration_speed

        self.motion(deltatime, self.position)

        if self.sprite is not None:
            self.render.image_ext(self.sprite, self.camera + self.position, self.size, -self.angle)

        return self.acceleration_timer <= 0 and self.acceleration.x < 1 and self.acceleration.y < 1
