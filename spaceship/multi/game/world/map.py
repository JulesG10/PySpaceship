import os
import random
import threading

from spaceship.engine.graphic import Renderer
from spaceship.engine.util import Vec, displayCalc


class Tile:
    SIZE = Vec(10, 10)

    def __init__(self, pos, sprite, render, camera):
        self.size = displayCalc.percentage(Tile.SIZE)
        self.sprite = sprite

        self.render = render
        self.camera = camera

        self.position = pos

    def draw(self):
        view = self.camera + self.position + self.size
        if view.x < 0 or view.x > displayCalc.width + self.size.x or view.y < 0 or view.y > displayCalc.height + self.size.y:
            return

        self.render.image_ext(self.sprite, self.camera + self.position, self.size)

class Chunk:

    SIZE = Vec(10, 10)

    def __init__(self, position, camera, render):
        self.camera = camera
        self.render = render

        self.tile_size = displayCalc.percentage(Tile.SIZE)
        self.size = Chunk.SIZE * self.tile_size
        self.position = position * self.size

        self.tiles = []

    def random_fill(self, render, sprites):
        for x in range(0, Chunk.SIZE.x):
            for y in range(0, Chunk.SIZE.y):

                random_sprite = sprites[random.randint(0, len(sprites)-1)]
                pos = self.position + Vec(x, y) * self.tile_size

                tile = Tile(pos, random_sprite, render, self.camera)
                self.tiles.append(tile)

    def get_static(self):
        static = self.render.image_fill((0, 0, 0), self.size)
        for tile in self.tiles:   
            self.render.blit(static, tile.sprite, (tile.position - self.position), tile.size)
        return static

    def is_visible(self):
        view = self.camera + self.position + self.size
        if view.x < 0 or view.x > displayCalc.width + self.size.x or view.y < 0 or view.y > displayCalc.height + self.size.y:
            return False
        return True

    def draw(self):
        if self.is_visible():
            for tile in self.tiles:
                tile.draw()


class Map:

    def __init__(self, renderer, camera):
        self.render = renderer
        self.camera = camera

        self.chunks = []
        self.tiles_sprite = []
        self.tile_size = displayCalc.percentage(Vec(10, 10))

        self.max_size = Vec(0,0)

        self.loading = True
        self.on_load = None
        self.loading_state = 0

        self.load_sprites()

        threading.Thread(target=self.load_tilemap, args=([""])).start()

    def load_sprites(self):
        tiles = os.listdir('./assets/tiles')
        TILE_START = 37

        for i in range(0, len(tiles)):
            if i >= TILE_START:
                self.tiles_sprite.append(
                    Renderer.load_image('./assets/tiles/'+tiles[i]))

    def load_tilemap(self, map): # TODO: load map
        size_x = 10
        size_y = 10

        for x in range(0, size_x):
            for y in range(0, size_y):
                chunk = Chunk(Vec(x, y), self.camera, self.render)
                chunk.random_fill(self.render, self.tiles_sprite)
                self.chunks.append(chunk)

                self.loading_state = round((x * size_y + y) / (size_x * size_y) * 100)
        
        self.loading_state = 100
        
        self.max_size = Vec(size_x, size_y) * self.chunks[0].size
        self.loading = False

        if self.on_load:
            self.on_load()

        

    def draw(self, deltatime):
        for chunk in self.chunks:
            chunk.draw()
