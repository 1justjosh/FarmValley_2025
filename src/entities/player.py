from psutil import swap_memory

from src.engine.settings import *
from src.engine.timer import Timer
from src.entities.entity import Entity
from src.tiles.tiles import Tile
from src.engine.utils import get_joystick_pressed,get_joystick_axis


class Player(Entity):
    def __init__(self,pos,frames,group,generator):
        super().__init__(pos,frames,group,generator)
        self.create()
        self.hitbox = pg.Rect(self.rect.midbottom, (TILE_SIZE * 0.5, TILE_SIZE * 0.5))

        self.use_tool = False
        self.selected_tool = 0
        self.tools = ["hoe", "water", "axe"]

        self.show_debug = False

        self.action_direction = {
            "right": (TILE_SIZE // 2, 0),
            "left": (-(TILE_SIZE // 2), 0),
            "down": (0, TILE_SIZE // 2),
            "up": (0 , -(TILE_SIZE // 2)),
        }

        self.timers["change-tool"] = Timer(500)
        self.timers["show_debug"] = Timer(250)

        self.joystick = None
        self.joystick_active = False
        self.check_joystick()

    def check_joystick(self):
        # Sanity check to avoid invalid index
        if pg.joystick.get_count() > 0:
            js = pg.joystick.Joystick(0)
            self.joystick = js

    def event_handler(self, event):
        if event.type == pg.KEYDOWN or event.type == pg.MOUSEMOTION:
            self.joystick_active = False

        if event.type == pg.JOYBUTTONDOWN:
            if get_joystick_pressed(self.joystick,7):
                self.generator.paused = not self.generator.paused
        if event.type == pg.JOYBUTTONDOWN or event.type == pg.JOYHATMOTION:
            self.joystick_active = True
        if event.type == pg.JOYDEVICEADDED:
            pg.joystick.quit()
            pg.joystick.init()

            self.check_joystick()


    def input(self):
        key = pg.key.get_pressed()
        if get_joystick_pressed(self.joystick,9) and get_joystick_pressed(self.joystick,8) or key[pg.K_F1]:
            if not self.timers["show_debug"].active:
                self.timers["show_debug"].activate()
                self.show_debug = not self.show_debug

        if not self.use_tool:
            self.anim_speed = 7
            if key[pg.K_SPACE] or get_joystick_pressed(self.joystick,0):
                self.anim_speed = 12
                self.use_tool = True
                self.index = 0

            if not self.timers["change-tool"].active:
                if key[pg.K_e] or get_joystick_pressed(self.joystick,4):
                    self.timers["change-tool"].activate()
                    self.selected_tool += 1
                    if self.selected_tool >= len(self.tools):
                        self.selected_tool = 0

                if key[pg.K_q] or get_joystick_pressed(self.joystick,5):
                    self.timers["change-tool"].activate()
                    self.selected_tool -= 1
                    if self.selected_tool < 0:
                        self.selected_tool = len(self.tools) -1

            # Movement Horizontal
            x_input = 0
            y_input = 0

            # Keyboard movement
            if key[pg.K_d]:
                x_input += 1
            elif key[pg.K_a]:
                x_input -= 1

            if key[pg.K_w]:
                y_input -= 1
            elif key[pg.K_s]:
                y_input += 1

            # Joystick input
            x_input += get_joystick_axis(self.joystick,0)  # left stick X
            y_input += get_joystick_axis(self.joystick,1)  # left stick Y

            self.direction.x = x_input
            self.direction.y = y_input

            # Update facing direction
            if self.direction.x > 0:
                self.status = "right"
            elif self.direction.x < 0:
                self.status = "left"
            elif self.direction.y > 0:
                self.status = "down"
            elif self.direction.y < 0:
                self.status = "up"

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

            action_x = self.hitbox.centerx + self.action_direction[self.status.split("_")[0]][0]
            action_y = self.hitbox.centery + self.action_direction[self.status.split("_")[0]][1]

            pos_key = f"{x};{y}"
            if (
                    self.selected_tool == 0
                    and pos_key not in self.generator.dirt_tiles
                    and pos_key in self.generator.plantable_rects
            ):
                tile = Tile((x, y), self.generator.assets["tiles"]["dirt"][12], self.visible_group, "dirt")
                self.generator.dirt_tiles[pos_key] = tile
                chunk_key = self.generator.get_chunk_key(x, y)
                self.generator.chunk_tiles[chunk_key]["dirt"].append(tile)

            if self.selected_tool == 2 and pos_key in self.generator.tree_tiles:

                tree = self.generator.tree_tiles[pos_key][1]
                tree_rect = self.generator.tree_tiles[pos_key][0]

                if tree_rect.collidepoint((action_x,action_y)):
                    print("Hit tree!")

            if int(self.index) + 1 >= len(self.frames[self.status]):
                self.use_tool = False


    def update(self,dt):
        super().update(dt)

        if not get_joystick_axis(self.joystick,0) == 0 or  not get_joystick_axis(self.joystick,1) == 0:
            self.joystick_active = True

        pg.mouse.set_visible(not self.joystick_active)
        pg.event.set_grab(self.joystick_active)

        self.input()
        self.get_status()
        self.tool_use()
        self.move(dt)


        self.animate(dt)

        self.end()