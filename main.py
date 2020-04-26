import pygame as pg
from Game import Game
from settings import *

pg.init()
pg.mixer.init()

g = Game()

while g.running:
    g.new_game()
    g.show_go_screen()
