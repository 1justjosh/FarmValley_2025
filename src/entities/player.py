from src.engine.settings import *
from src.engine.timer import Timer
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

        self.timers["change-tool"] = Timer(500)

        self.joystick = None
        self.check_joystick()

    def check_joystick(self):
        # Sanity check to avoid invalid index
        if pg.joystick.get_count() > 0:
            js = pg.joystick.Joystick(0)
            self.joystick = js

    def event_handler(self, event):
        if event.type == pg.JOYDEVICEADDED:
            pg.joystick.quit()
            pg.joystick.init()

            self.check_joystick()

    def get_joystick_pressed(self,number):
        if not self.joystick:
            return False

        return self.joystick.get_button(number)

    def get_joystick_axis(self, axis_num, deadzone=0.8):
        if not self.joystick:
            return 0

        value = self.joystick.get_axis(axis_num)
        return value if abs(value) > deadzone else 0

    def input(self):
        key = pg.key.get_pressed()
        if not self.use_tool:

            if key[pg.K_SPACE] or self.get_joystick_pressed(0):
                self.use_tool = True
                self.index = 0

            if not self.timers["change-tool"].active:
                if key[pg.K_e] or self.get_joystick_pressed(4):
                    self.timers["change-tool"].activate()
                    self.selected_tool += 1
                    if self.selected_tool >= len(self.tools):
                        self.selected_tool = 0

                if key[pg.K_q] or self.get_joystick_pressed(5):
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
            x_input += self.get_joystick_axis(0)  # left stick X
            y_input += self.get_joystick_axis(1)  # left stick Y

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

            if self.selected_tool == 0 and not self.generator.dirt_tiles.get(f"{x};{y}",False):
                tile = Tile((x, y), self.generator.assets["dirt"][12], self.visible_group, "dirt")
                self.generator.dirt_tiles[f"{x};{y}"] = tile
                chunk_key = self.generator.get_chunk_key(x, y)
                self.generator.chunk_tiles[chunk_key]["dirt"].append(tile)

            if int(self.index) + 1 >= len(self.frames[self.status]):
                self.use_tool = False


    def update(self,dt):
        super().update(dt)
        self.input()
        self.get_status()
        self.tool_use()
        self.move(dt)


        self.animate(dt)

        self.end()