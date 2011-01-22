"""
beeld test file. kloot maar aan.
"""
import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

class entertainment_menu:
	def __init__(self, width=800, height=600):
		"""Initialize"""
		"""Initialize PyGame"""
		pygame.init()
		"""Set the window Size"""
		self.width = width
		self.height = height
		"""Create the Screen"""
		#pygame.display.set_mode((80,60),pygame.FULLSCREEN)
		self.screen = pygame.display.set_mode((800,600),0)
		self.load_sprites()
        
	def load_sprites(self):
		"""Load the sprites that we need"""
		self.game_button = games_button()
		self.game_button_sprite = pygame.sprite.RenderPlain((self.game_button))

	def main_loop(self):
		for x in xrange(100):
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					sys.exit()
			self.game_button_sprite.draw(self.screen)
			pygame.display.flip()

class button(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		pygame.sprite.Sprite.__init__(self) 
		self.image, self.rect = load_image(image,-1)
		self.rect.move_ip(x, y)

def load_image(name, colorkey=None):
	fullname = os.path.dirname(sys.argv[0])
	fullname = os.path.join(fullname, 'images')
	fullname = os.path.join(fullname, name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error, message:
		print 'Cannot load image:', fullname, '. ', message
		raise SystemExit, message
	image = image.convert()
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
		image.set_colorkey(colorkey, RLEACCEL)
	return image, image.get_rect()

class games_button(button):
	def __init__(self):
		button.__init__(self, 'games.png',200,150)

if __name__ == "__main__":
	window = entertainment_menu()
	window.main_loop()
