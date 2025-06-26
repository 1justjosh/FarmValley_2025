from src.engine.settings import *
from src.engine.utils import load_tile_map


class HUD:
    def __init__(self,generator):
        self.win = pg.display.get_surface()

        self.generator = generator

        self.tool_selected_frame = load_tile_map("assets/images/emojis/emoji style ui/Inventory_Blocks_Spritesheet.png",48,48,scale=(128,128))[0]
        self.tool_selected_frame_rect = self.tool_selected_frame.get_rect(topleft=(0,0))

        tool_selected_icons = load_tile_map("assets/images/Objects/Items/tools-n-meterial-items.png",16,16,scale=(64,64))

        self.tool_selected_icons = [tool_selected_icons[2],tool_selected_icons[0],tool_selected_icons[1]]
        self.tool_selected_icons_rect = self.tool_selected_icons[0].get_rect(center=self.tool_selected_frame_rect.center)

    def render(self):
        self.win.blit(self.tool_selected_frame,self.tool_selected_frame_rect)
        self.win.blit(self.tool_selected_icons[self.generator.player.selected_tool],self.tool_selected_icons_rect)