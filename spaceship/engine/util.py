from math import radians, cos, sin, sqrt, floor, ceil
import math


class Vec:

    def __init__(self, x, y):
        self.x = x
        self.y = y


    @staticmethod
    def null():
        return Vec(0, 0)

    def dist(self, other):
        return sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2)

    def normalize(self):
        length = self.length()

        if length == 0:
            return Vec(0, 0)
        else:
            return Vec(self.x / length, self.y / length)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def cross(self, other):
        return self.x * other.y - self.y * other.x

    def rotate(self, angle):
        rad = radians(angle)
        cos = cos(rad)
        sin = sin(rad)
        return Vec(self.x * cos - self.y * sin, self.x * sin + self.y * cos)

    def rotate_around(self, angle, point):
        return self.rotate(angle) + point

    def is_null(self):
        return self.x == 0 and self.y == 0

    def __str__(self):
        return 'Vec({}, {})'.format(self.x, self.y)

    def __lt__(self, other):
        return self.x < other.x and self.y < other.y

    def __le__(self, other):
        return self.x <= other.x and self.y <= other.y

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y

    def __gt__(self, other):
        return self.x > other.x and self.y > other.y

    def to_tuple(self):
        return (self.x, self.y)

    def to_list(self):
        return [self.x, self.y]

    def to_dict(self):
        return {'x': self.x, 'y': self.y}

    def from_angle(self, angle):
        self.x = cos(radians(angle))
        self.y = sin(radians(angle))
        

    def from_dict(self, dict):
        self.x = dict['x']
        self.y = dict['y']

    def from_tuple(self, tuple):
        self.x = tuple[0]
        self.y = tuple[1]

    def from_list(self, list):
        self.x = list[0]
        self.y = list[1]

    def from_str(self, str):
        str = str.replace('Vec(', '').replace(')', '')
        parts = str.split(',')
        
        if len(parts) == 2:
            try:
                self.x = float(parts[0])
                self.y = float(parts[1])
            except ValueError:
                pass

        return self

    def __repr__(self):
        return 'Vec({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y

    def __add__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x + other.x, self.y + other.y)
        return Vec(self.x + other, self.y + other)

    def __sub__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x - other.x, self.y - other.y)
        return Vec(self.x - other, self.y - other)
        
    def __mul__(self, other):
        if isinstance(other, Vec):
           return Vec(self.x * other.x, self.y * other.y)
        return Vec(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Vec):
            return Vec(self.x / other.x, self.y / other.y)
        return Vec(self.x / other, self.y / other)

    def __floordiv__(self, other):
        return Vec(self.x // other, self.y // other)

    def __mod__(self, other):
        return Vec(self.x % other, self.y % other)

    def __pow__(self, other):
        return Vec(self.x ** other, self.y ** other)

    def __neg__(self):
        return Vec(-self.x, -self.y)

    def __pos__(self):
        return Vec(+self.x, +self.y)

    def __abs__(self):
        return Vec(abs(self.x), abs(self.y))

    def __invert__(self):
        return Vec(-self.x, -self.y)

    def __round__(self):
        return Vec(round(self.x), round(self.y))

    def __floor__(self):
        return Vec(floor(self.x), floor(self.y))

    def __ceil__(self):
        return Vec(ceil(self.x), ceil(self.y))


class DisplayCalculations:

    def __init__(self):
        self.width = 0
        self.height = 0
        

    def percentage(self, position, size=Vec(0,0)):
        w, h = size.x, size.y
        x, y = position.x, position.y

        if size.is_null():
            w = self.width
            h = self.height

        return round(Vec(w * x / 100, h * y / 100))
        
    def pixel(self, position, size=Vec(0, 0)):
        w, h = size.x, size.y
        x, y = position.x, position.y

        if size.is_null():
            w = self.width
            h = self.height

        return Vec(w * 100 / x, h * 100 / y)

    def center(self, size=Vec(0, 0)):
        return Vec((self.width - size.x)/ 2,( self.height - size.y)/ 2)


class Direction:
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    NONE = 4


def AABB(pos1, pos2, size1, size2):
    return pos1.x < pos2.x + size2.x and pos1.x + size1.x > pos2.x and pos1.y < pos2.y + size2.y and pos1.y + size1.y > pos2.y


displayCalc = DisplayCalculations()
