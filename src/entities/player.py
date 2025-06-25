from src.engine.settings import *
from src.entities.entity import Entity
from src.tiles.tiles import Tile


class Player(Entity):
    def __init__(self,pos,frames,group,generator):
        super().__init__(pos,frames,group,generator)
        self.create()
        self.hitbox = pg.Rect(self.rect.center, (TILE_SIZE * 0.9, TILE_SIZE * 0.9))

        self.use_tool = False
        self.selected_tool = 0
        self.tools = ["hoe", "water", "axe"]

        self.action_direction = {
            "right": (TILE_SIZE // 2, 0),
            "left": (-(TILE_SIZE // 2), 0),
            "down": (0, TILE_SIZE // 2),
            "up": (0 , -(TILE_SIZE // 2)),
        }

    def input(self):
        key = pg.key.get_pressed()

        if key[pg.K_SPACE]:
            if not self.use_tool:
                self.use_tool = True
                self.index = 0

        if not self.use_tool:

            # Movement Horizontal
            if key[pg.K_d]:
                self.direction.x = 1
                self.status = "right"
            elif key[pg.K_a]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            # Movement Vertical
            if key[pg.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif key[pg.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

    def get_status(self):
        if self.use_tool:
            self.status = self.status.split("_")[0] + "_" + self.tools[self.selected_tool]
            self.direction = pg.Vector2()
        elif self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"
        else:
            self.direction = self.direction.normalize()

    def tool_use(self):
        if self.use_tool:
            self.direction.x = 0
            self.direction.y = 0
            x = int((self.hitbox.centerx + self.action_direction[self.status.split("_")[0]][0]) // TILE_SIZE) * TILE_SIZE
            y = int((self.hitbox.centery + self.action_direction[self.status.split("_")[0]][1]) // TILE_SIZE) * TILE_SIZE

            if self.selected_tool == 0 and not self.generator.dirt_tiles.get(f"{x};{y}",False):
                tile = Tile((x, y), self.generator.assets["dirt"][12], self.visible_group, "dirt")
                self.generator.dirt_tiles[f"{x};{y}"] = tile
                chunk_key = self.generator.get_chunk_key(x, y)
                self.generator.chunk_tiles[chunk_key]["dirt"].append(tile)

            print(len(self.generator.dirt_tiles))
            if int(self.index) + 1 >= len(self.frames[self.status]):
                self.use_tool = False


    def update(self,dt):
        self.input()
        self.get_status()
        self.tool_use()
        self.move(dt)


        self.animate(dt)

        self.end()