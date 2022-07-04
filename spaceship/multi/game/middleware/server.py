import time
import logging
import sys

from threading import Thread
from spaceship.engine.util import Vec
from spaceship.multi.game.entity.bullet import Bullet
from spaceship.multi.game.entity.core import Entity
from spaceship.multi.game.entity.player import Player

from spaceship.multi.game.middleware.channels import GameChannel
from spaceship.multi.tcp.server import Server

class GameServer:

    def __init__(self, console=False):

        self.logger = logging.getLogger()

        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%m-%d-%Y %H:%M:%S')
        stdout = logging.StreamHandler(sys.stdout)

        if console:
            self.logger.setLevel(logging.DEBUG)
        else:
            stdout.setLevel(logging.NOTSET)

        stdout.setFormatter(formatter)
        self.logger.addHandler(stdout)

        self.server = Server()
        self.game_thread = None

        self.players: list[Player] = []
        self.bullets: list[Bullet] = []
        self.id = 0

        self.server.on(GameChannel.CLIENT_ADD, self.new_player)
        self.server.on(GameChannel.CLIENT_REMOVE, self.quit_player)

        self.server.on(GameChannel.CLIENT_PLAYER, self.player_state_update)

        self.server.on(GameChannel.CLIENT_BULLET, self.new_bullet)
        self.server.on(GameChannel.CLIENT_BULLET_REMOVE, self.remove_bullet)
        self.server.on(GameChannel.CLIENT_UPDATE_BULLET, self.update_bullet)
        # self.server.on(GameChannel.CLIENT_HIT, self.player_hit_bullet)

    def has_error(self):
        return self.server.last_error != ""

    def get_error(self):
        return self.server.last_error

    def count_clients(self):
        return len(self.server.clients)

    def get_code(self):
        return self.server.code

    def alive(self):
        return self.server.active

    def start(self):
        result = self.server.start()

        self.game_thread = Thread(target=self.start_game)
        self.game_thread.start()

        return result

    def close(self):
        self.logger.info("Closing server")
        self.server.close()

    def reset(self):
        self.server.reset()


    def start_game(self):
        self.logger.info("Starting server")
        self.logger.info("Code: {0}".format(self.server.code))

        SERVER_TICKS = 144
        
        while self.alive():
            for player in self.players:
                result = self.server.send(GameChannel.CLIENT_UPDATE, self.get_update(player), player.socket)
                if not result and player in self.players:
                    self.players.remove(player)
                    self.logger.info("Client {0}:{1} disconnected".format(player.address[0], player.address[1]))
                    
            # time.sleep(1/SERVER_TICKS)

    def get_update(self, player: Player):
        player_states = []
        bullet_states = []

        for pl in self.players:
            if pl.id != player.id:
                player_states.append(pl.state)

        for bullet in self.bullets:
            bullet_states.append(bullet.state)

        update = {
            "id": player.id,
            "players": player_states,
            "bullets": bullet_states
        }
        return update

    def player_state_update(self, data, client, addr):
        player = self.get_player(addr)
        if player:
            csize = Vec.null()
            csize.from_dict(data['client_size'])
            
            player.state = Entity.vec_from_client(data, 'position', csize)
           

    def new_bullet(self, data, client, addr):
        player = self.get_player(addr)
        if player:
            self.id += 1
            bullet = Bullet.create_server(0, 0,  Vec.null(), Vec.null())
            
            csize = Vec.null()
            csize.from_dict(data['client_size'])

            bullet.state = Entity.vec_from_client(data, 'position', csize)

            bullet.id = self.id
            bullet.owner = player.id

            self.bullets.append(bullet)

    def update_bullet(self, data, client, addr):
        for bullet in self.bullets:
            if bullet.id == data['id']:

                csize = Vec.null()
                csize.from_dict(data['client_size'])
                
                bullet.state = Entity.vec_from_client(data, 'position')

    def remove_bullet(self, data, client, addr):
        for bullet in self.bullets:
            if bullet.id == data["id"]:
                self.bullets.remove(bullet)
                break

    # def player_hit_bullet(self, data, client, addr):
    #     for bullet in self.bullets:
    #         if bullet.id == data["id"]:
    #             self.bullets.remove(bullet)
    #             break


    def get_player(self, addr):
        for player in self.players:
                if player.address == addr:
                    return player
        return None

    def new_player(self, data, client, addr):
        
        self.id += 1

        cposition = Vec.null()
        csize = Vec.null()

        player = Player.create_server(self.id, cposition, 0, 100, csize)

        player.address = addr
        player.socket = client

        self.players.append(player)
        self.logger.info("Client {0}:{1} connected".format(addr[0], addr[1]))

    def quit_player(self, data, client, addr):
        player = self.get_player(addr)
        if player:
            for bullet in self.bullets:
                if bullet.owner == player.id:
                    self.bullets.remove(bullet)
            self.players.remove(player)
            self.logger.info("Client {0}:{1} disconnected".format(addr[0], addr[1]))
