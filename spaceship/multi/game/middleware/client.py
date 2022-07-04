from spaceship.multi.game.middleware.channels import GameChannel
from spaceship.multi.tcp.client import Client

class GameClient:

    WAIT = 0
    RUN = 1
    ERROR = -1

    def __init__(self, host):
        self.host = host
        
        self.wait_for_connect = GameClient.WAIT

        self.client = Client(self.host)
        self.client.set_connect_callback(self.on_client_connect)
        self.client.set_error_callback(self.on_client_error)
        
        self.client.start()
        self.client.on(GameChannel.CLIENT_UPDATE, self.entities_update)
        
        self.on_update = None
       

    def has_error(self):
        return self.client.last_error != ""

    def get_error(self):
        return self.client.last_error

    def close(self):
        self.client.send(GameChannel.CLIENT_REMOVE, 0)
        self.client.close()

    def on_client_error(self):
        self.wait_for_connect = GameClient.ERROR

    def on_client_connect(self):
        self.wait_for_connect = GameClient.RUN
        self.client.send(GameChannel.CLIENT_ADD, 0)

    def entities_update(self, entities):
        if self.on_update is not None:
            self.on_update(entities)



    def send_bullet(self, bullet):
        self.client.send(GameChannel.CLIENT_BULLET, bullet)

    def send_update_bullet(self, bullet):
        self.client.send(GameChannel.CLIENT_UPDATE_BULLET, bullet)

    def send_update_player(self, player):
        self.client.send(GameChannel.CLIENT_PLAYER, player)

    def send_bullet_remove(self, bullet_id):
        self.client.send(GameChannel.CLIENT_BULLET_REMOVE, {"id": bullet_id})



    def pause(self):
        self.client.send(GameChannel.CLIENT_PAUSE, 1)

    def resume(self):
        self.client.send(GameChannel.CLIENT_PAUSE, 0)
