import os.path
import random

from src.engine.camera import Camera
from src.engine.settings import *
from src.engine.utils import load_tile_map
from src.entities.player import Player
from src.tiles.animated_tile import AnimatedTile
from src.tiles.tiles import Tile
from pytmx.util_pygame import load_pygame

from src.tiles.tree import Tree
from src.ui.hud import HUD

from collections import defaultdict

class Generator:
    def __init__(self):
        self.win = pg.display.get_surface()

        self.chunk_size = TILE_SIZE
        self.chunk_tiles = defaultdict(lambda: defaultdict(list))  # {chunk_key: {z: [tiles]}}

        self.paused = False

        self.visible_sprites = Camera(self)
        self.collide_rects = {}
        self.plantable_rects = {}
        self.dirt_tiles = {}
        self.tree_tiles = {}

        self.assets = self.load_assets()

        self.player = None

        self.hud = HUD(self,self.assets["HUD"])

        self.map = load_pygame(os.path.join(WORLD_PATH, "overworld", "personal_farm.tmx"))
        self.load_all()

    @staticmethod
    def load_assets():
        base_player = load_tile_map(os.path.join(IMAGE_PATH,"Characters","Premium Charakter Spritesheet.png"),48,48,scale=(TILE_SIZE * 2,TILE_SIZE * 2))
        dirt_tile = load_tile_map(os.path.join(IMAGE_PATH,"Tilesets","ground tiles","Old tiles","Tilled_Dirt_Wide_v2.png"),16,16,scale=(TILE_SIZE,TILE_SIZE))
        emote_tile = load_tile_map(os.path.join(IMAGE_PATH,"UI Sprites","Dialouge UI","Emotes","Teemo premium emote animations sprite sheet-export.png"),32,32,scale=(76,76))
        tree_tiles = load_tile_map(os.path.join(IMAGE_PATH,"Objects","Trees, stumps and bushes.png"),16,16,scale=(TILE_SIZE,TILE_SIZE))
        fruit_tiles = load_tile_map(os.path.join(IMAGE_PATH,"Objects","Items","fruit-n-berries-items.png"),16,16,scale=(TILE_SIZE//3,TILE_SIZE//3))
        big_tree = load_tile_map(os.path.join(IMAGE_PATH,"Objects","Tree animations","tree_sprites.png"),48,48,scale=(TILE_SIZE*2,TILE_SIZE*2))
        small_tree = pg.Surface((TILE_SIZE,TILE_SIZE*2),flags=pg.SRCALPHA)
        small_tree.blit(tree_tiles[0],(0,0))
        small_tree.blit(tree_tiles[12],(0,TILE_SIZE))

        return {
            "player": {
                "down_idle": base_player[0:7],
                "down": base_player[32:39],
                "down_hoe": base_player[96:103],
                "down_axe": base_player[128:135],
                "down_water": base_player[160:167],

                "up_idle": base_player[8:15],
                "up": base_player[40:47],
                "up_hoe": base_player[104:111],
                "up_axe": base_player[136:143],
                "up_water": base_player[168:176],

                "left_idle": base_player[24:32],
                "left": base_player[56:64],
                "left_hoe": base_player[120:128],
                "left_axe": base_player[152:160],
                "left_water": base_player[184:192],

                "right_idle": base_player[16:24],
                "right": base_player[48:56],
                "right_hoe": base_player[112:120],
                "right_axe": base_player[144:152],
                "right_water": base_player[176:184],

            },
            "tiles": {
                "dirt": dirt_tile,
                "trees": {
                    "fruit": {
                        "apple": fruit_tiles[0],
                        "peach": pg.transform.scale(tree_tiles[30],(TILE_SIZE//2,TILE_SIZE//2))
                    },
                    "small": small_tree,
                    "big":{
                        "idle": [big_tree[0]],
                        "pop-up": big_tree[12:15],
                        "shake": big_tree[24:29]
                    }
                }
            },
            "HUD":{
                "frames": load_tile_map("assets/images/emojis/emoji style ui/Inventory_Blocks_Spritesheet.png",48,48,scale=(128,128)),
                "tools": load_tile_map("assets/images/Objects/Items/tools-n-meterial-items.png",16,16,scale=(64,64)),
                "emote": {
                    "pop-up": emote_tile[:12],
                    "pop-down": emote_tile[13:20],
                    "idle": [emote_tile[26]],
                    "tongue-out": emote_tile[39:40],
                    "floppy-ears": emote_tile[52:56]
                }
            }
        }

    def regenerate_chunk(self, chunk_key):
        # 1. Clear chunk data
        if chunk_key in self.chunk_tiles:
            for layer in self.chunk_tiles[chunk_key].values():
                layer.clear()

        # 2. Recalculate world coordinates from chunk_key
        chunk_x, chunk_y = map(int, chunk_key.split(";"))
        world_x = chunk_x * self.chunk_size
        world_y = chunk_y * self.chunk_size

        # 3. Reload plantable/floor (optional depending on design)
        # self.load_layer("floor")  # Careful: this loads full layer; might need a localized one

        # 4. Reload trees in that area only
        self.load_trees_in_area(world_x, world_y)

    def load_trees_in_area(self, chunk_world_x, chunk_world_y):
        buffer = self.chunk_size

        for layer in self.map.layers:
            if not hasattr(layer, "tiles") or not layer.name.endswith("_trees"):
                continue

            chance = layer.properties.get("chance", 1)
            tree_type = layer.properties.get("type", "apple")

            for x, y, img in layer.tiles():
                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE

                # Check if tree is within the chunk region
                if not (chunk_world_x <= world_x < chunk_world_x + buffer and
                        chunk_world_y <= world_y < chunk_world_y + buffer):
                    continue

                pos_key = f"{world_x};{world_y}"
                right_pos_key = f"{world_x + TILE_SIZE};{world_y}"

                if random.randint(0, chance) != 0:
                    continue

                if pos_key in self.plantable_rects and right_pos_key in self.plantable_rects:
                    tree = Tree(
                        (world_x, world_y - TILE_SIZE),
                        self.assets["tiles"]["trees"]["big"],
                        [],
                        self,
                        tree_type,
                        self.assets["tiles"]["trees"]["fruit"][tree_type]
                    )

                    chunk_key = self.get_chunk_key(world_x, world_y - TILE_SIZE)
                    self.chunk_tiles[chunk_key]["main"].append(tree)

                    trunk_width = TILE_SIZE * 0.5
                    trunk_height = TILE_SIZE * 0.6
                    trunk_x = world_x + TILE_SIZE - trunk_width / 2
                    trunk_y = world_y + TILE_SIZE - trunk_height * 0.9

                    tree_hitbox = pg.Rect(
                        trunk_x,
                        trunk_y - TILE_SIZE / 4,
                        trunk_width,
                        trunk_height
                    )

                    self.collide_rects[pos_key] = tree_hitbox
                    self.tree_tiles[pos_key] = [tree_hitbox, tree]
                    self.tree_tiles[right_pos_key] = [tree_hitbox, tree]

                    del self.plantable_rects[pos_key]
                    del self.plantable_rects[right_pos_key]

    def load_all(self):
        self.load_layer("plantable","floor")
        self.load_layer("floor")
        self.load_trees()
        self.load_layer("water",animated_frames=load_tile_map("assets/images/Tilesets/ground tiles/water frames/Water.png",16,16,scale=(TILE_SIZE,TILE_SIZE)))
        self.load_layer("world-end")
        self.load_objects("entities","player")

    def load_trees(self):
        for layer in self.map.layers:
            if not hasattr(layer, "tiles"):
                continue
            if not layer.name.endswith("_trees"):
                continue

            chance = layer.properties.get("chance", 1)
            tree_type = layer.properties.get("type", "apple")

            for x, y, img in layer.tiles():
                if random.randint(0, chance) != 0:
                    continue

                world_x = x * TILE_SIZE
                world_y = y * TILE_SIZE
                pos_key = f"{world_x};{world_y}"
                right_pos_key = f"{world_x + TILE_SIZE};{world_y}"

                # Reserve both base tiles to prevent overlap
                if pos_key in self.plantable_rects and right_pos_key in self.plantable_rects:
                    # Anchor top-left of 2×2 image
                    tree = Tree(
                        (world_x, world_y - TILE_SIZE),  # top-left corner
                        self.assets["tiles"]["trees"]["big"],
                        [],
                        self,
                        tree_type,
                        self.assets["tiles"]["trees"]["fruit"][tree_type]
                    )

                    chunk_key = self.get_chunk_key(world_x, world_y - TILE_SIZE)
                    self.chunk_tiles[chunk_key]["main"].append(tree)


                    trunk_width = TILE_SIZE * 0.5
                    trunk_height = TILE_SIZE * 0.6

                    trunk_x = world_x + TILE_SIZE - trunk_width / 2
                    trunk_y = world_y + TILE_SIZE - trunk_height * 0.9  # slightly up from the ground

                    tree_hitbox = pg.Rect(
                        trunk_x,
                        trunk_y - TILE_SIZE / 4,
                        trunk_width,
                        trunk_height
                    )

                    self.collide_rects[pos_key] = tree_hitbox

                    self.tree_tiles[pos_key] = [tree_hitbox,tree]
                    self.tree_tiles[right_pos_key] = [tree_hitbox,tree]

                    # Remove from plantable
                    del self.plantable_rects[pos_key]
                    del self.plantable_rects[right_pos_key]

    def load_objects(self,layer_name,name):
        for obj in self.map.get_layer_by_name(layer_name):
            x = int(obj.x // self.map.tilewidth) * TILE_SIZE
            y = int(obj.y // self.map.tileheight) * TILE_SIZE
            if obj.name == "Player":
                self.player = Player((x, y), self.assets["player"], self.visible_sprites,self)

    def get_chunk_key(self, x, y):
        return f"{x // self.chunk_size};{y // self.chunk_size}"

    def load_layer(self, name ,z=None, animated_frames:list=None):
        for x, y, img in self.map.get_layer_by_name(name).tiles():
            world_x = x * TILE_SIZE
            world_y = y * TILE_SIZE
            img = pg.transform.scale(img, (TILE_SIZE, TILE_SIZE))

            if name == "plantable":
                self.plantable_rects[f"{world_x};{world_y}"] = pg.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)

            if name in COLLIDE_LAYERS:
                self.collide_rects[f"{world_x};{world_y}"] = pg.Rect(world_x, world_y, TILE_SIZE, TILE_SIZE)
            else:
                z_value = name if z is None else z


                if animated_frames:
                    tile = AnimatedTile((world_x, world_y), animated_frames, [], z_value)
                else:
                    tile = Tile((world_x, world_y), img, [], z_value)

                chunk_key = self.get_chunk_key(world_x, world_y)
                self.chunk_tiles[chunk_key][z_value].append(tile)

    def event_handler(self, event):
        self.player.event_handler(event)

    def update(self, dt):
        self.visible_sprites.update(dt)
        self.hud.update(dt)

    def render(self):
        self.visible_sprites.render(self.player)
        self.hud.render()
