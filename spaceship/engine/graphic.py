import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
os.environ['SDL_VIDEO_CENTERED'] = '1'

import pygame
import pygame.gfxdraw
from pygame import *
from spaceship.engine.util import Vec

class Empty:
    pass

class Renderer:

    def __init__(self, window):
        self.win = window
        self.sprites = []
        
        self.fonts = self.load_font('ebrima')
        if len(self.fonts) == 0:
            self.fonts = self.load_font('arial')

    @property
    def height(self):
        return self.win.height

    @property
    def width(self):
        return self.win.width

    @property
    def renderer(self):
        return self.win.renderer

    def clear(self):
        self.win.renderer.fill((0, 0, 0))

    def load_font(self, fontName_pathFont, fontLen=6, fontStep=12):
        fonts = []

        if fontName_pathFont in pygame.font.get_fonts():
            for i in range(1, fontLen+1):
                font = pygame.font.SysFont(fontName_pathFont, i*fontStep)
                fonts.append(font)

        elif os.path.exists(fontName_pathFont):
            for i in range(1, fontLen+1):
                font = pygame.font.Font(fontName_pathFont, i*fontStep)
                fonts.append(font)
        else:
            return []

        return fonts


    def text_sprite(self, value, size=1, color=(0, 0, 0), fonts=[]):
        if len(self.fonts) == 0 and len(fonts) == 0:
            return

        font = self.fonts[size % len(self.fonts)]
        if len(fonts) != 0:
            font = fonts[size % len(fonts)]

        return font.render(value, True, color)
        
    def text(self, value, position, size=1, color=(0, 0, 0), center=False, fonts=[]):
        x,y = position.x, position.y
        if len(self.fonts) == 0 and len(fonts) == 0:
            return

        font = self.fonts[size % len(self.fonts)]
        if len(fonts) != 0:
            font = fonts[size % len(fonts)]

        text= font.render(value, True, color)
            
        textRect = text.get_rect()
        if center:
            textRect.center = (x, y)
        else:
            textRect.top = y
            textRect.left = x

        self.win.renderer.blit(text, textRect)
        return font.size(value)

    def text_size(self, value, size, fonts=[]):
        if len(self.fonts) == 0 and len(fonts) == 0:
            return
        font = self.fonts[size % len(self.fonts)]
        if len(fonts) != 0:
            font = fonts[size % len(fonts)]
        return font.size(value)



    def _findimage(self, image):
        for s in self.sprites:
            if s[0] == image:
                return s[1]
        return None

    def image_ext(self, surface, position, size=Vec.null(), rotation=0, scale=1, flip=(False, False)):
        texture = None
        
        if size.is_null():
            size.x = surface.get_width()
            size.y = surface.get_height()

        texture = transform.scale(surface, (int(size.x * scale),
                                            int(size.y * scale)))
        if rotation != 0:
            texture = transform.rotate(texture, rotation)
            rect = texture.get_rect(center = (position.x + size.x/2, position.y + size.y/2))
            
            position = Vec(rect.x, rect.y)

        if flip[0]:
            texture = pygame.transform.flip(texture, True, False)

        if flip[1]:
            texture = pygame.transform.flip(texture, False, True)

        self.win.renderer.blit(
            texture, (position.x, position.y))

    def image(self, image, position):
        x,y = position.x, position.y
        texture = image
        if type(texture) == str:
            texture = self._findimage(image)
            if texture is None:
                texture = pygame.image.load(image)
                self.sprites.append([image, texture])

        self.win.renderer.blit(texture, (x, y))

    @staticmethod
    def load_images(dirname, extension=['png', 'jpg', 'jpeg']):
        images = []
        for file in os.listdir(dirname):
            if file.split('.')[-1] in extension:
                image = pygame.image.load(os.path.join(dirname, file)).convert_alpha()
                images.append(image)
        return images

    @staticmethod
    def split_image(image, size):
        images = []
        img = Renderer.load_image(image)
        for y in range(0, img.get_height(), size.y):
            for x in range(0, img.get_width(), size.x):
                images.append(img.subsurface((x, y, size.x, size.y)))
        return images

    @staticmethod
    def load_image(image):
        if os.path.exists(image):
            img = pygame.image.load(image).convert_alpha()
            return img
        return None


    def line(self, pos1, pos2, color, width=1):
        x1, y1, x2, y2 = pos1.x, pos1.y, pos2.x, pos2.y
        pygame.draw.line(self.win.renderer, color, (x1, y1), (x2, y2), width)
    
    def blit(self, parent_surf, child_surf, position, size):
        x,y = position.x, position.y
        w,h = size.x, size.y
        scaled = transform.scale(child_surf, (w, h))
        parent_surf.blit(scaled, (x, y), (0, 0, w, h))
        

    def image_fill(self, color, size):
        surface = pygame.Surface((size.x, size.y)).convert_alpha()
        surface.fill(color)
        return surface

    def alpha(self, surface, position, alpha=255):
        x, y = position.x, position.y
        surface.set_alpha(alpha)
        self.win.renderer.blit(surface, (x, y))

    def rectangle(self, position, size, color, borderRadius=0):
        x, y = position.x, position.y
        width, height = size.x, size.y
        
        rect = pygame.Rect(x, y, width, height)

        border_rad = borderRadius
        if rect.width < border_rad*2 or rect.height < 2*border_rad:
            border_rad = 0
        
        if border_rad == 0:
            pygame.draw.rect(self.win.renderer, color, rect)
        else:
            pygame.gfxdraw.aacircle(
                self.win.renderer, rect.left+border_rad, rect.top+border_rad, border_rad, color)
            pygame.gfxdraw.aacircle(
                self.win.renderer, rect.right-border_rad-1, rect.top+border_rad, border_rad, color)
            pygame.gfxdraw.aacircle(
                self.win.renderer, rect.left+border_rad, rect.bottom-border_rad-1, border_rad, color)
            pygame.gfxdraw.aacircle(
                self.win.renderer, rect.right-border_rad-1, rect.bottom-border_rad-1, border_rad, color)

            pygame.gfxdraw.filled_circle(
                self.win.renderer, rect.left+border_rad, rect.top+border_rad, border_rad, color)
            pygame.gfxdraw.filled_circle(
                self.win.renderer, rect.right-border_rad-1, rect.top+border_rad, border_rad, color)
            pygame.gfxdraw.filled_circle(
                self.win.renderer, rect.left+border_rad, rect.bottom-border_rad-1, border_rad, color)
            pygame.gfxdraw.filled_circle(
                self.win.renderer, rect.right-border_rad-1, rect.bottom-border_rad-1, border_rad, color)

            rect_tmp = pygame.Rect(rect)

            rect_tmp.width -= 2 * border_rad
            rect_tmp.center = rect.center
            pygame.draw.rect(self.win.renderer, color, rect_tmp)

            rect_tmp.width = rect.width
            rect_tmp.height -= 2 * border_rad
            rect_tmp.center = rect.center
            pygame.draw.rect(self.win.renderer, color, rect_tmp)

    def border(self, position, size, color, line_size=1):
        x,y = position.x, position.y
        width, height = size.x, size.y

        self.line(Vec(x, y), Vec(x+width, y), color, line_size)
        self.line(Vec(x+width, y), Vec(x+width,  y+height), color, line_size)
        self.line(Vec(x, y+height), Vec(x+width, y+height), color, line_size)
        self.line(Vec(x, y), Vec(x, y+height), color, line_size)

    def circle(self,position, radius, color, border=0):
        x, y = position.x, position.y
        pygame.draw.circle(self.win.renderer, color, (x, y), radius, border)


    @staticmethod
    def create_surface_renderer(surface):
        window = Empty()
        
        setattr(window, 'renderer', surface)
        setattr(window, 'width', surface.get_width())
        setattr(window, 'height', surface.get_height())

        renderer = Renderer(window)
        return renderer
