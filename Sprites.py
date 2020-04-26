import pygame as pg
from settings import * 

class Spritesheet:
	def __init__(self, path):
		self.spritesheet = pg.image.load(path).convert()

	def get_image(self, x, y, w, h):
		image = pg.Surface((w, h))
		image.blit(self.spritesheet, (0, 0), (x, y, w, h))
		image = pg.transform.scale(image, (w//3, h//3))

		return image

class Trex(pg.sprite.Sprite):
	def __init__(self, game):
		self._layer = TREX_LAYER
		self.groups = game.sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		
		self.game = game
		self.image = self.game.spritesheet.get_image(60, 20, 250, 280)
		self.image = pg.transform.flip(self.image, True, False)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.can_jump = True

		self.pos = pg.math.Vector2(self.rect.width/2 + 50, pg.display.get_surface().get_size()[1])
		self.vel = pg.math.Vector2(0, 0)
		self.acc = pg.math.Vector2(0, GRAVITY)

		self.mask = pg.mask.from_surface(self.image)

	def update(self):
		self.acc = pg.math.Vector2(0, GRAVITY)

		keys = pg.key.get_pressed()

		if keys[pg.K_SPACE]:
			self.jump()

		self.vel += self.acc

		self.pos.y += self.vel.y

		self.pos += (1/2)*self.acc+self.vel 
		self.rect.midbottom = self.pos

	def jump(self):
		if self.can_jump:
			if pg.sprite.collide_rect(self, self.game.ground):
				self.game.jump_sound.play()
				self.vel.y = -JUMP_FORCE

class Obstacle(pg.sprite.Sprite):
	def __init__(self, game, x):
		self._layer = OBSTACLE_LAYER
		self.groups = game.sprites, game.obstacles
		pg.sprite.Sprite.__init__(self, self.groups)

		self.game = game
		self.image = self.game.spritesheet.get_image(390, 20, 150, 280)
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = pg.display.get_surface().get_size()[1] - self.game.ground.rect.height - 55
		self.stop = False

		self.vel = 10

		self.mask = pg.mask.from_surface(self.image)

	def update(self):
		if not self.stop:
			self.rect.x -= self.vel

		if self.game.score % 50 == 0 and self.game.score != 0 and self.game.score < 500:
			self.vel += 2

		if self.rect.x < -50:
			self.kill()

class Ground(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self._layer = GROUND_LAYER
		self.groups = game.sprites
		pg.sprite.Sprite.__init__(self, self.groups)

		self.game = game

		self.image = pg.Surface((w, h))
		self.image.fill(GROUND_COLOR)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

