from spaceship.engine.util import displayCalc, Vec

class Camera:

    def __init__(self, position, origin = Vec.null()):
        self.position = position
        self.origin = origin
        self.reset_origin = Vec.null()        
        self.size = Vec(displayCalc.width, displayCalc.height)

    def __add__(self, other):
        return self.position + other

    def __sub__(self, other):
        return self.position - other

    def set_origin(self,origin):
        self.origin = origin
        self.reset_origin = origin


    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        self.position.x = value

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        self.position.y = value
