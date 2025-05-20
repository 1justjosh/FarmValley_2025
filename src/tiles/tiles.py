from src.engine.settings import *

class Tile(pg.sprite.Sprite):
    def __init__(self,pos,img,group,z):
        super().__init__(group)
        self.z = z
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)