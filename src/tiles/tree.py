import random

from src.engine.settings import *
from src.tiles.tiles import Tile

class Tree(Tile):
    def __init__(self,pos,img,group,generator,tree_type,fruit_img):
        super().__init__(pos, img["idle"][0], group, "main")
        self.image = img["idle"][0].copy()

        self.index = 0
        self.anim_speed = 4
        self.status = "idle"
        self.frames = img

        self.tree_type = tree_type
        self.generator = generator
        
        self.num_fruit = random.randint(0,3)
        self.fruit_img = fruit_img

        self.placed_position = []
        self.load_fruit()

        self.hit = False

    def load_fruit(self):
        canopy_top = TILE_SIZE * 0.6  # skip empty upper part
        canopy_bottom = TILE_SIZE * 1.5  # upper 1.5 tiles of 2×2 tree
        max_x = self.image.get_width() - self.fruit_img.get_width() - 40
        max_y = canopy_bottom - self.fruit_img.get_height()

        min_distance = self.fruit_img.get_width()
        placed_positions = []
        attempts = 0

        while len(placed_positions) < self.num_fruit and attempts < 50:
            x = random.randint(40, max_x)
            y = random.randint(int(canopy_top), int(max_y))
            pos = (x, y)

            too_close = any(math.hypot(x - px, y - py) < min_distance for px, py in placed_positions)

            if not too_close:
                self.placed_position.append(pos)
                placed_positions.append(pos)

            attempts += 1

    def animate(self,dt):
        self.index += self.anim_speed * dt

        if self.index >= len(self.frames[self.status]):
            self.index = 0

        self.image = self.frames[self.status][int(self.index)].copy()

        for pos in self.placed_position:
            self.image.blit(self.fruit_img, pos)

    def get_status(self):
        if not self.hit:
            self.status = "pop-up"

    def update(self,dt):
        self.get_status()
        self.animate(dt)



