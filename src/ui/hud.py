from src.engine.settings import *
from src.ui.inventory_gui import InventoryGUI


class HUD:
    def __init__(self,generator,assets):
        self.win = pg.display.get_surface()

        self.generator = generator
        self.assets = assets


        self.emote_frame = self.assets["frames"]["general"][7]
        self.emote_frame_rect = self.emote_frame.get_rect(topleft=(0,0))

        self.emote_status = "pop-up"
        self.emote_index = 0
        self.emote_anim_speed = 7
        self.change_emote_status = False
        self.emote_image = self.assets["emote"][self.emote_status][self.emote_index]
        self.emote_rect = self.emote_image.get_rect(center=self.emote_frame_rect.center)

        self.tool_selected_frame = self.assets["frames"]["general"][0]
        self.tool_selected_frame_rect = self.tool_selected_frame.get_rect(topleft=vec2(self.emote_frame_rect.topleft) + vec2(128,0))

        tool_selected_icons = self.assets["tools"]

        self.tool_selected_icons = [tool_selected_icons[2],tool_selected_icons[0],tool_selected_icons[1]]
        self.tool_selected_icons_rect = self.tool_selected_icons[0].get_rect(center=self.tool_selected_frame_rect.center)

        self.player_inventory_gui = InventoryGUI(self.generator)

    def animate_emote(self, dt):
        frames = self.assets["emote"][self.emote_status]
        self.emote_index += self.emote_anim_speed * dt

        if int(self.emote_index) >= len(frames):
            self.emote_index = len(frames) - 1  # clamp on last frame
            self.change_emote_status = True
        else:
            self.emote_image = frames[int(self.emote_index)]

    def check_emote_status(self):
        if self.change_emote_status:
            self.emote_index = 0
            self.change_emote_status = False
            if self.emote_status == "pop-up":
                self.emote_status = "pop-down"
            elif self.emote_status == "pop-down":
                self.emote_status = "pop-up"

    def update(self,dt):
        self.check_emote_status()
        self.animate_emote(dt)

    def render(self):
        self.win.blit(self.emote_frame,self.emote_frame_rect)
        self.win.blit(self.emote_image,self.emote_rect)
        self.win.blit(self.tool_selected_frame,self.tool_selected_frame_rect)
        self.win.blit(self.tool_selected_icons[self.generator.player.selected_tool],self.tool_selected_icons_rect)

        self.player_inventory_gui.render()

