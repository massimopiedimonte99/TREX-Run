import pygame as pg
import random
from os import path

from Sprites import *
from settings import *

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((W, H))
        self.screen.fill(BG_COLOR)
        pg.display.set_caption(TITLE)
        
        self.running = True
        self.dir = path.dirname(__file__)
        self.dir_sound = path.join(self.dir, "sounds")

        self.font_name = path.join(path.join(self.dir, "font"), FONT_NAME)

        self.jump_sound = pg.mixer.Sound(path.join(self.dir_sound, "jump.wav"))
        self.score_sound = pg.mixer.Sound(path.join(self.dir_sound, "score.wav"))
        self.die_sound = pg.mixer.Sound(path.join(self.dir_sound, "die.wav"))

        self.load_data()

    def load_data(self):
        self.spritesheet = Spritesheet(path.join(path.join(self.dir, 'img'), 'spritesheet.png'))
      
    def new_game(self):
        self.playing = True
        self.sprites = pg.sprite.LayeredUpdates()
        self.obstacles = pg.sprite.Group()
        self.obstacles_pos = []
        self.score = 0
        self.last_increase = 0
        self.can_increase = True

        self.last_spawn = 0

        self.ground = Ground(self, 0, H-100, W, 100)
        self.trex = Trex(self)

        for i in range(5):
            if len(self.obstacles_pos) > 0:
                obstacle = Obstacle(self, self.obstacles_pos[-1] + random.randrange(150, W))
            else:
                obstacle = Obstacle(self, W+random.randrange(100, W))

            self.obstacles_pos.append(obstacle.rect.right)

        for obstacle in self.obstacles:
            obstacle.stop = False
        
        self.trex.can_jump = True

        self.run()

    def events(self):
        for evt in pg.event.get():
            if evt.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    
    def draw(self):
        self.screen.fill(BG_COLOR)
        self.show_score()
        self.sprites.draw(self.screen)
        
        pg.display.flip()
    
    def update(self):
        self.sprites.update()

        hits = pg.sprite.collide_rect(self.trex, self.ground)
        if hits:
            self.trex.pos.y = self.ground.rect.top + 30
            self.trex.vel.y = 0

        hits = pg.sprite.spritecollide(self.trex, self.obstacles, False, pg.sprite.collide_mask)
        if hits:
            self.die_sound.play()
            for obstacle in self.obstacles:
                obstacle.stop = True
            self.trex.can_jump = False
            self.can_increase = False
            self.playing = False

        if self.score % 50 == 0 and self.score != 0:
            self.score_sound.play()

        if len(self.obstacles) < 5:
            obstacle = Obstacle(self, self.obstacles_pos[-1])
            self.obstacles_pos.append(obstacle.rect.right)

        if self.can_increase:
            now = pg.time.get_ticks()
            if now - self.last_increase > 100:
                self.last_increase = now
                self.score += 1

    def show_go_screen(self):
        self.draw_text("GAME OVER", BLACK, 30, W//2, H//2)
        self.draw_text("Press a key to restart", BLACK, 20, W//2, H//2+50)
        pg.display.flip()

        self.wait()

    def wait(self):
        r = True
        while r:
            for evt in pg.event.get():
                if evt.type == pg.QUIT: 
                    r = False
                    self.running = False
                if evt.type == pg.KEYDOWN:
                    r = False

    def show_score(self):
        self.draw_text(str(self.score).zfill(5), BLACK, 30, W-80, 10)

    def draw_text(self, text, color, fsize, x, y):
        font = pg.font.Font(self.font_name, fsize)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        while self.playing:
            pg.time.Clock().tick(FPS)  
            
            self.events()
            self.update()
            self.draw()