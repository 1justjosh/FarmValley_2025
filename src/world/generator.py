from src.engine.camera import Camera
from src.engine.settings import *
from src.engine.utils import load_tile_map
from src.entities.player import Player
from src.tiles.animated_tile import AnimatedTile
from src.tiles.tiles import Tile
from pytmx.util_pygame import load_pygame
from src.ui.hud import HUD

from collections import defaultdict

class Generator:
    def __init__(self):
        self.win = pg.display.get_surface()

        self.chunk_size = TILE_SIZE
        self.chunk_tiles = defaultdict(lambda: defaultdict(list))  # {chunk_key: {z: [tiles]}}


        self.visible_sprites = Camera(self)
        self.collide_rects = {}
        self.plantable_rects = {}
        self.dirt_tiles = {}

        self.assets = self.load_assets()

        self.player = None

        self.hud = HUD(self,self.assets["HUD"])

        self.map = load_pygame(os.path.join(WORLD_PATH, "overworld", "personal_farm.tmx"))
        self.load_all()

    @staticmethod
    def load_assets():
        base_player = load_tile_map(os.path.join(IMAGE_PATH,"Characters","Premium Charakter Spritesheet.png"),48,48,scale=(TILE_SIZE * 2,TILE_SIZE * 2))
        dirt_tile = load_tile_map(os.path.join(IMAGE_PATH,"Tilesets","ground tiles","Old tiles","Tilled_Dirt_Wide_v2.png"),16,16,scale=(TILE_SIZE,TILE_SIZE))
        emote_tile = load_tile_map(os.path.join(IMAGE_PATH,"UI Sprites/Dialouge UI/Emotes/Teemo premium emote animations sprite sheet-export.png"),32,32,scale=(76,76))
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
                    "dirt":dirt_tile,
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

    def load_all(self):
        self.load_layer("plantable","floor")
        self.load_layer("water",animated_frames=load_tile_map("assets/images/Tilesets/ground tiles/water frames/Water.png",16,16,scale=(TILE_SIZE,TILE_SIZE)))
        self.load_layer("world-end")
        self.load_objects("entities","player")

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
