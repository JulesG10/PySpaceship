from copy import copy
import random

from spaceship.engine.graphic import Renderer
from spaceship.engine.util import displayCalc, Vec
from spaceship.multi.game.entity.bullet import Bullet
from spaceship.multi.game.entity.core import Entity, WorldCoord
from spaceship.multi.game.entity.enemy import Enemy
from spaceship.multi.game.entity.player import Player

from spaceship.multi.game.middleware.client import GameClient
from spaceship.multi.game.world.camera import Camera
from spaceship.multi.game.world.map import Map

from spaceship.screen.core import ScreenData


class World:

    def __init__(self, renderer: Renderer, client: GameClient, data=ScreenData()):
        self.render = renderer
        self.data = data

        self.client = client
        self.client.on_update = self.on_update

        self.camera = Camera(Vec.null())
        self.map = Map(self.render, self.camera)
        self.map.on_load = self.map_loaded

        pos = Vec(1000, 100)
        wpos = WorldCoord.format(pos, self.camera.size)
        self.player = Player.create_client(
            wpos, Player.LV_1, self.on_player_shoot, self.map, self.render, self.camera)

        origin_base = displayCalc.percentage(Vec(50, 90))
        origin_base.x -= self.player.size.x / 2
        origin_base.y -= self.player.size.y

        self.camera.set_origin(origin_base)

        self.player.set_keys({
            "key_left": self.data.get("key_left", ord('q')),
            "key_right": self.data.get("key_right", ord('d')),
            "key_up": self.data.get("key_up", ord('z')),
            "key_down": self.data.get("key_down", ord('s')),
            "key_fire": self.data.get("key_fire", ord(' '))
        })

        self.bullets: list[Bullet] = []
        self.players: list[Player] = []

        self.shake_timer = 0
        self.update_timer = 10

    def shake(self, magnitude):
        self.camera.origin.x += random.randint(-magnitude, magnitude)
        self.camera.origin.y += random.randint(-magnitude, magnitude)

    def reset_origin(self):
        self.camera.origin = copy(self.camera.reset_origin)

    def label(self, text, position, color=(255, 255, 255), center=False):
        return self.render.text(text, position, 1, color, center)

    def on_player_shoot(self, bullet):
        if self.player.id != Entity.ID_NOTSET:
            self.client.send_bullet(bullet.state)
            # self.bullets.append(bullet)

    def map_loaded(self):
        self.player.position = Vec((self.map.max_size.x - self.player.size.x)/2, self.map.max_size.y - self.player.size.y)

    def on_update(self, entities):
        self.player.id = entities["id"]

        for bullet in self.bullets:
            if bullet.id not in [new_b['id'] for new_b in entities['bullets']]:
                self.bullets.remove(bullet)

        for player in self.players:
            if player.id not in [new_p['id'] for new_p in entities['players']]:
                self.players.remove(player)

        for b_obj in entities['bullets']:
            if b_obj['id'] not in [bullet.id for bullet in self.bullets]:

                wpos = Vec.null()
                wpos.from_dict(b_obj['position'])
                wpos = WorldCoord.convert(wpos, self.camera.size)

                bullet = Bullet.create_client(
                    wpos, b_obj['angle'], self.render, self.camera)
                bullet.state = Entity.vec_from_server(
                    b_obj, 'position', self.camera.size)
                self.bullets.append(bullet)

        for p_obj in entities["players"]:
            if p_obj['id'] not in [player.id for player in self.players]:
                enemy = Enemy.create_client(Vec.null(), p_obj['level'], self.render, self.camera)
                enemy.state = Entity.vec_from_server(p_obj, 'position', self.camera.size)
                self.players.append(enemy)
            else:
                for player in self.players:
                    if player.id == p_obj['id']:
                        player.state = Entity.vec_from_server(p_obj, 'position', self.camera.size)
                        
                        player.set_level(p_obj['level'])

    def draw(self, input, deltatime):
        if self.client.wait_for_connect == GameClient.RUN:

            if self.map.loading:
                self.render.rectangle(Vec.null(), Vec(
                    self.render.width, self.render.height), self.data.get("background_color", (0, 0, 0)))

                self.label("Loading map...",
                           displayCalc.percentage(Vec(50, 40)), (255, 255, 255), True)

                self.label("{}%".format(self.map.loading_state),
                           displayCalc.percentage(Vec(50, 50)), (255, 255, 255), True)

                return

            if self.shake_timer > 0:
                self.shake_timer -= deltatime * 100
                self.reset_origin()
                self.shake(2)
            else:
                self.reset_origin()

            self.map.draw(deltatime)

            for bullet in self.bullets:
                if bullet.draw(input, deltatime):
                    self.client.send_bullet_remove(bullet.id)

            for player in self.players:
                player.draw(input, deltatime)

            self.player.draw(input, deltatime)

            if self.update_timer > 0:
                self.update_timer -= deltatime * 100
            else:
                self.update_timer = 10
                
                self.client.send_update_player(self.player.state)

                for bullet in self.bullets:
                    if bullet.owner == self.player.id:
                        self.client.send_update_bullet(bullet.state)
