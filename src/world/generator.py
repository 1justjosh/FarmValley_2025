from src.engine.camera import Camera
from src.engine.settings import *
from src.engine.utils import load_tile_map
from src.entities.player import Player
from src.tiles.animated_tile import AnimatedTile
from src.tiles.tiles import Tile
from pytmx.util_pygame import load_pygame

from collections import defaultdict

class Generator:
    def __init__(self):
        self.win = pg.display.get_surface()

        self.chunk_size = TILE_SIZE
        self.chunk_tiles = defaultdict(lambda: defaultdict(list))  # {chunk_key: {z: [tiles]}}


        self.visible_sprites = Camera(self)
        self.collide_rects = {}


        self.assets = self.load_assets()

        self.player = None

        self.map = load_pygame(os.path.join(WORLD_PATH, "overworld", "personal_farm.tmx"))
        self.load_all()

    @staticmethod
    def load_assets():
        base_player = load_tile_map(os.path.join(IMAGE_PATH,"Characters","Premium Charakter Spritesheet.png"),48,48,scale=(TILE_SIZE * 2,TILE_SIZE * 2))

        return {
            "player": {
                "down_idle": [base_player[0], base_player[1], base_player[2], base_player[3], base_player[4],
                              base_player[5], base_player[6], base_player[7]],
                "down": [base_player[32], base_player[33], base_player[34], base_player[35], base_player[36],
                         base_player[37], base_player[38], base_player[39]],
                "down_hoe": [base_player[96], base_player[97], base_player[98], base_player[99], base_player[100],
                             base_player[101], base_player[102], base_player[103]],
                "down_axe": [base_player[128], base_player[129], base_player[130], base_player[131], base_player[132],
                             base_player[133], base_player[134], base_player[135]],
                "down_water": [base_player[160], base_player[161], base_player[162], base_player[163], base_player[164],
                               base_player[165], base_player[166], base_player[167]],
                "up_idle": [base_player[8], base_player[9], base_player[10], base_player[11], base_player[12],
                            base_player[13], base_player[14], base_player[15]],
                "up": [base_player[40], base_player[41], base_player[42], base_player[43], base_player[44],
                       base_player[45], base_player[46], base_player[47]],
                "up_hoe": [base_player[104], base_player[105], base_player[106], base_player[107], base_player[108],
                           base_player[109], base_player[110], base_player[111]],
                "up_axe": [base_player[136], base_player[137], base_player[138], base_player[139], base_player[140],
                           base_player[141], base_player[142], base_player[143]],
                "up_water": [base_player[168], base_player[169], base_player[170], base_player[171], base_player[172],
                             base_player[173], base_player[174], base_player[175]],
                "left_idle": [base_player[24], base_player[25], base_player[26], base_player[27], base_player[28],
                              base_player[29], base_player[30], base_player[31]],
                "left": [base_player[56], base_player[57], base_player[58], base_player[59], base_player[60],
                         base_player[61], base_player[62], base_player[63]],
                "left_hoe": [base_player[120], base_player[121], base_player[122], base_player[123], base_player[124],
                             base_player[125], base_player[126], base_player[127]],
                "left_axe": [base_player[152], base_player[153], base_player[154], base_player[155], base_player[156],
                             base_player[157], base_player[158], base_player[159]],
                "left_water": [base_player[184], base_player[185], base_player[186], base_player[187], base_player[188],
                               base_player[189], base_player[190], base_player[191]],
                "right_idle": [base_player[16], base_player[17], base_player[18], base_player[19], base_player[20],
                               base_player[21], base_player[22], base_player[23]],
                "right": [base_player[48], base_player[49], base_player[50], base_player[51], base_player[52],
                          base_player[53], base_player[54], base_player[55]],
                "right_hoe": [base_player[112], base_player[113], base_player[114], base_player[115], base_player[116],
                              base_player[117], base_player[118], base_player[119]],
                "right_axe": [base_player[144], base_player[145], base_player[146], base_player[147], base_player[148],
                              base_player[149], base_player[150], base_player[151]],
                "right_water": [base_player[176], base_player[177], base_player[178], base_player[179],
                                base_player[180], base_player[181], base_player[182], base_player[183]],
            },
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
        pass

    def update(self, dt):
        self.visible_sprites.update(dt)

    def render(self):
        self.visible_sprites.render(self.player)
