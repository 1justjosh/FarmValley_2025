from src.engine.settings import *

class Entity(pg.sprite.Sprite):
    def __init__(self,pos,frames,group):
        super().__init__(group)
        self.z = "entities"

        self.frames = frames
        self.status = "down_idle"
        self.index = 0
        self.anim_speed = 7

        self.start_pos = pos
        self.direction = pg.math.Vector2()
        self.speed = 500

        self.image = None
        self.rect = None
        self.hitbox = None
        self.old_rect = None

    def create(self):
        self.image = self.frames[self.status][int(self.index)]
        self.rect = self.image.get_rect(center=self.start_pos)
        self.hitbox = self.rect.copy()
        self.old_rect = self.hitbox.copy()

    def animate(self,dt):
        self.index += self.anim_speed * dt
        if self.index >= len(self.frames[self.status]):
            self.index = 0

        self.image = self.frames[self.status][int(self.index)]

    def move(self,dt):
        self.hitbox.x += self.direction.x * self.speed * dt
        self.hitbox.y += self.direction.y * self.speed * dt

        self.rect.center = self.hitbox.center