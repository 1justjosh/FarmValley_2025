from src.engine.settings import *

class Entity(pg.sprite.Sprite):
    def __init__(self,pos,frames,group,generator):
        super().__init__(group)
        self.z = "entities"

        self.timers = {}

        self.visible_group = group

        self.generator = generator

        self.frames = frames
        self.status = "down_idle"
        self.index = 0
        self.anim_speed = 7

        self.start_pos = pos
        self.direction = pg.math.Vector2()
        self.speed = 500

        self.collide_objects = []

        self.image = None
        self.rect = None
        self.hitbox = None
        self.old_rect = None

    def create(self, hitbox=None):
        self.image = self.frames[self.status][int(self.index)]
        self.rect = self.image.get_rect(center=self.start_pos)

        if not hitbox:
            self.hitbox = self.rect.copy().inflate(-TILE_SIZE / 2, -TILE_SIZE / 2)
        else:
            self.hitbox = hitbox
            self.hitbox.center = self.rect.center

        self.rect.center = self.hitbox.center  # <-- Force rect to follow hitbox
        self.old_rect = self.hitbox.copy()

    def event_handler(self,event): ...

    def end(self):
        self.old_rect = self.hitbox.copy()

    def get_tile_position(self):
        tile_x = int(self.hitbox.centerx // TILE_SIZE)
        tile_y = int(self.hitbox.centery // TILE_SIZE)
        return tile_x, tile_y

    def get_surrounding_collide_tiles(self):
        # Get player's current tile position
        tile_x, tile_y = self.get_tile_position()

        surrounding = []

        # Check 3x3 grid around the player (including center)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                check_x = (tile_x + dx) * TILE_SIZE
                check_y = (tile_y + dy) * TILE_SIZE
                key = f"{check_x};{check_y}"

                if key in self.generator.collide_rects:
                    surrounding.append(self.generator.collide_rects[key])

        return surrounding

    def collide(self, direction):
        for tile in self.collide_objects:
            if self.hitbox.colliderect(tile):
                if direction == "H":
                    if self.hitbox.left <= tile.right <= self.old_rect.left:
                        self.hitbox.left = tile.right
                    if self.hitbox.right >= tile.left >= self.old_rect.right:
                        self.hitbox.right = tile.left
                else:
                    if self.direction.y > 0:
                        self.hitbox.bottom = tile.top
                    if self.direction.y < 0:
                        self.hitbox.top = tile.bottom

    def animate(self, dt):
        self.index += self.anim_speed * dt
        if self.index >= len(self.frames[self.status]):
            self.index = 0

        self.image = self.frames[self.status][int(self.index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def move(self,dt):
        self.old_rect = self.hitbox.copy()

        self.collide_objects = []
        self.collide_objects = self.get_surrounding_collide_tiles()

        self.hitbox.x += self.direction.x * self.speed * dt
        self.collide("H")
        self.hitbox.y += self.direction.y * self.speed * dt
        self.collide("V")


        self.rect.center = self.hitbox.center
        self.old_rect = self.hitbox.copy()

    def update(self,dt):
        for timer in self.timers.values():
            timer.update()