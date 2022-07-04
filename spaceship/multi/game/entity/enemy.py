import os

from spaceship.engine.graphic import Renderer
from spaceship.engine.util import Vec, displayCalc
from spaceship.multi.game.entity.core import Entity, WorldCoord


class Enemy(Entity):

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

    @staticmethod
    def create_client(wposition, level, render, camera):
        enemy = Enemy()
        enemy.position = WorldCoord.convert(wposition, camera.size)

        enemy.camera = camera
        enemy.render = render

        enemy.set_level(level)

        return enemy

    @staticmethod
    def create_server(id, cposition, level, life, csize):
        enemy = Enemy()
        enemy.id = id

        enemy.life = life
        enemy.level = level

        enemy.position = WorldCoord.format(cposition, csize)

        return enemy

    def __init__(self):
        Entity.__init__(self)

        self.size = displayCalc.percentage(Vec(20, 20))

        self.id = Entity.ID_NOTSET
        self.life = 100
        self.level = 0

    def draw(self, input, deltatime):
        if self.sprite is not None:
            
            self.render.image_ext(self.sprite, self.camera + self.position, self.size, self.angle)

    def set_level(self, level):
        spriteIndexStart = 12
        spriteIndexEnd = 24

        self.level = (level + spriteIndexStart)%spriteIndexEnd

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
