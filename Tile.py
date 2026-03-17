import pygame as pag
from Utilidades_pygame import obj_base

class Tile:
    def __init__(self, position, mine=False):
        self.position = position
        self.state = "idle"
        self.mine = mine
        self.neightbors = 0
