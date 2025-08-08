import random

from src.engine.settings import *
from src.tiles.tiles import Tile
from src.engine.timer import Timer


class Tree(Tile):
    def __init__(self, pos, img, group, generator, tree_type, fruit_img):
        super().__init__(pos, img["idle"][0], group, "main")
        self.image = img["idle"][0].copy()

        self.index = 0
        self.anim_speed = 4
        self.status = "idle"
        self.frames = img

        self.tree_type = tree_type
        self.generator = generator

        self.num_fruit = random.randint(0, 3)
        self.fruit_img = fruit_img
        self.health = self.num_fruit + 3 # 3 health for tree and added more health per fruit taken away

        self.placed_position = []
        self.load_fruit()

        self.mask = pg.mask.from_surface(self.image)
        self.tree_mask = self.mask.to_surface()
        self.tree_mask.set_colorkey((0,0,0))

        self.flash = False
        self.is_hit = False
        self.timers["tree_flash"] = Timer(100)


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

    def animate(self, dt):
        self.index += self.anim_speed * dt

        if self.index >= len(self.frames[self.status]):
            self.index = 0

        self.image = self.frames[self.status][int(self.index)].copy()

        for pos in self.placed_position:
            self.image.blit(self.fruit_img, pos)

    def hit(self):
            if self.health > 3: # we have fruit remainder
                if len(self.placed_position) > 0:
                    self.placed_position.pop(0)
            else: # attack tree
                self.timers["tree_flash"].activate()


            self.health -= 1

            if self.health <= 0:
                base_x, base_y = self.rect.topleft
                pos_key = f"{base_x};{base_y + TILE_SIZE}"  # original pos_key
                right_pos_key = f"{base_x + TILE_SIZE};{base_y + TILE_SIZE}"

                chunk_key = self.generator.get_chunk_key(self.rect.x, self.rect.y)

                if chunk_key in self.generator.chunk_tiles:
                    layer = self.generator.chunk_tiles[chunk_key].get("main", [])
                    if self in layer:
                        layer.remove(self)

                del self.generator.collide_rects[pos_key]

                del self.generator.tree_tiles[pos_key]
                del self.generator.tree_tiles[right_pos_key]
                self.kill()


    def update(self, dt):
        super().update(dt)
        if not self.timers["tree_flash"].active:
            self.animate(dt)
        else:
            self.image = self.tree_mask