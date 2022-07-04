
import random

from spaceship.engine.util import Direction, Vec, displayCalc
from spaceship.entity.explosion import Explosion
from spaceship.entity.player import Player
from spaceship.gui.core import Style
from spaceship.screen.core import ScreenItem, Screens, style_button
from spaceship.entity.enemy import Enemy
from spaceship.gui.range import Range

class Solo(ScreenItem):

    def __init__(self, renderer, data):
        ScreenItem.__init__(self, renderer, data)

        self.background = self.render.load_image(
            './assets/backgrounds/desert-backgorund.png')
        self.bg_position = Vec(0, 0)
        self.bg_speed = 100

        self.enemy_spawn_time = 100
        self.enemy_spawn_timer = 0
        self.enemies = []

        self.player = Player(self.render)
        self.bullets = []
        self.explosions = []

        self.data.get("key_left", ord('q'))
        self.data.get("key_right", ord('d'))
        self.data.get("key_up", ord('z'))
        self.data.get("key_down", ord('s'))
        self.data.get("key_fire", ord(' '))
        self.data.get("key_pause", ord('p'))

        self.player.set_keys(self.data.get("key_left"), self.data.get(
            "key_right"), self.data.get("key_fire"))

        life_style  =Style()
        life_style.color = (200, 30, 30)
        life_style.borderColor = (30, 30, 30)
        life_style.borderSize = 2
        self.life_range = Range(self.render, displayCalc.percentage(
            Vec(20, 4)), Vec(10, 10), self.player.life, life_style)

        self.blur = self.render.image_fill((100,100,100), displayCalc.percentage(Vec(100,100)))

        self.pause = False
        self.play_button = style_button(
            renderer, "Play", displayCalc.percentage(Vec(50, 40)))
        self.back_button = style_button(
            renderer, "Exit Game", displayCalc.percentage(Vec(50, 60)))

    def background_animation(self, deltatime):
        self.bg_position.y += deltatime * self.bg_speed
        if self.bg_position.y >= displayCalc.percentage(Vec(0, 100)).y:
            self.bg_position.y = 0

        self.render.image_ext(self.background, self.bg_position, Vec(
            displayCalc.width, displayCalc.height))
        self.render.image_ext(self.background,
                              Vec(0, -displayCalc.height + self.bg_position.y),
                              Vec(displayCalc.width, displayCalc.height))

    def spawn_enemy(self, deltatime):
        self.enemy_spawn_timer += deltatime * 100
        if self.enemy_spawn_timer >= self.enemy_spawn_time:
            self.enemy_spawn_timer = 0

            type = random.choice([Enemy.SMALL, Enemy.MEDIUM, Enemy.BIG])

            if type == Enemy.SMALL:
                self.enemy_spawn_time = 200
            elif type == Enemy.MEDIUM:
                self.enemy_spawn_time = 300
            else:
                self.enemy_spawn_time = 375
            self.enemies.append(Enemy(self.render, type))

    def draw_enemies(self, deltatime):
        for enemy in self.enemies:
            vec = enemy.draw(self, deltatime)
            if not vec.is_null() or not enemy.collision(self.player.position, self.player.size).is_null():
                if vec.is_null():
                    self.player.life -= enemy.die_damage
                    self.player.score += 50

                self.enemies.remove(enemy)
                self.explosions.append(Explosion(self.render, enemy.position))

    def draw_bullets(self, deltatime):
        for bullet in self.bullets:
            if not bullet.draw(deltatime):
                self.bullets.remove(bullet)
            elif bullet.direction == Direction.DOWN and bullet.collision(self.player.position, self.player.size):
                self.player.life -= bullet.damage
                if not bullet.alive:
                    self.bullets.remove(bullet)
            else:
                for enemy in self.enemies:
                    if bullet.direction == Direction.UP and bullet.collision(enemy.position, enemy.size):
                        enemy.life -= bullet.damage
                        if enemy.life <= 0:
                            self.player.add_kill()
                            self.enemies.remove(enemy)
                            self.explosions.append(
                                Explosion(self.render, enemy.position))
                        if not bullet.alive:
                            self.bullets.remove(bullet)
                        break

    def draw_explosions(self, deltatime):
        for explosion in self.explosions:
            if explosion.draw(deltatime):
                self.explosions.remove(explosion)

    def draw(self, input, deltatime):
        ScreenItem.draw(self, input, deltatime)
        if input.key_tap(self.data.get("key_pause")):
            self.pause = not self.pause

        if self.pause:
            self.background_animation(0)

            self.render.alpha(self.blur, Vec(0, 0), 200)
            if self.back_button.draw(input, deltatime):
                return Screens.HOME
            if self.play_button.draw(input, deltatime):
                self.pause = False
            
            return
            
            
        self.background_animation(deltatime)

        self.spawn_enemy(deltatime)
        self.draw_enemies(deltatime)

        self.draw_bullets(deltatime)
        self.draw_explosions(deltatime)

        if not self.player.draw(self, input, deltatime).is_null():
            self.data.set("player", {"kill":self.player.kill, "score": self.player.score })
            return Screens.GAMEOVER
        else:
            self.player.score += deltatime
            self.life_range.value = self.player.life

        self.life_range.draw(input,deltatime)
        self.render.text("Score " + str(round(self.player.score, 2)),
                         displayCalc.percentage(Vec(2, 8)), 1, (200, 200, 200))
        if self.player.kill:
            self.render.text("Kill " + str(self.player.kill),
                                displayCalc.percentage(Vec(2, 16)), 1, (200, 200, 200))

        
