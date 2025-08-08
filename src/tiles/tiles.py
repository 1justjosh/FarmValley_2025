from src.engine.settings import *
from src.engine.timer import Timer

class Tile(pg.sprite.Sprite):
    def __init__(self,pos,img,group,z):
        super().__init__(group)
        self.z = z
        self.image = img
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()
        self.old_rect = self.hitbox

        self.timers:dict[str,Timer] = {}

    def update(self,dt):
        for timer in self.timers.values():
            timer.update()