from spaceship.engine.util import displayCalc, Vec


class WorldCoord:

    SIZE = Vec(1000, 1000)

    @staticmethod
    def format(client_coordinates, client_size):
        pos = Vec.null()

        try:
            pos.x = client_coordinates.x * WorldCoord.SIZE.x / client_size.x
            pos.y = client_coordinates.y * WorldCoord.SIZE.y / client_size.y
        except:
            return client_coordinates

        return pos

    @staticmethod
    def convert(world_coordinates, client_size):
        pos = Vec.null()

        try:
            pos.x = world_coordinates.x * client_size.x / WorldCoord.SIZE.x
            pos.y = world_coordinates.y * client_size.y / WorldCoord.SIZE.y
        except:
            return world_coordinates

        return pos

class Entity:
    ID_NOTSET = -1
    
    def __init__(self):
        self.sprite = None
        self.render = None
        self.camera = None

        self.size = Vec.null()
        self.position = Vec.null()

        self.friction = Vec(-5, -5)
        
        self.velocity = Vec.null()
        self.acceleration = Vec.null()
        
        self.angle = 0

        self.client_size = Vec(displayCalc.width, displayCalc.height)

    @staticmethod
    def vec_from_server(state, field, size):
        cpos = Vec.null()
        cpos.from_dict(state[field])
        cpos = WorldCoord.convert(cpos, size)

        state[field] = cpos.to_dict()
        return state

    def vec_from_client(state, field, size):
        wpos = Vec.null()
        wpos.from_dict(state[field])
        wpos = WorldCoord.format(wpos, size)

        state[field] = wpos.to_dict()
        return state

    @staticmethod
    def create_client():
        pass

    @staticmethod
    def create_server():
        pass

    def motion(self, deltatime, position):
        self.acceleration += self.velocity * self.friction
        self.velocity += self.acceleration * deltatime

        position.x += (self.velocity.x * deltatime) + \
            (self.acceleration.x * 0.5) * (deltatime ** 2)
        position.y += (self.velocity.y * deltatime) + \
            (self.acceleration.y * 0.5) * (deltatime ** 2)

    def reset_acceralation(self):
        self.acceleration.x = 0
        self.acceleration.y = 0

    def draw(self, input, deltatime):
        pass


    @property
    def state(self):
        pass

    @state.setter
    def state(self,state):
        pass
