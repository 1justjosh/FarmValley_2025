from src.engine.settings import *


class Camera(pg.sprite.Group):
    def __init__(self):
        super().__init__()

        self.win = pg.display.get_surface()
        self.offset = pg.math.Vector2()


    def render(self, player):
        self.offset.x = player.hitbox.centerx + 50 - WIDTH / 2
        self.offset.y = player.hitbox.centery + 50 - HEIGHT / 2
        for layer in LAYERS:
            for sprites in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
                if sprites.z == layer:
                    offset_rect = sprites.rect.copy()
                    offset_rect.center -= self.offset

                    self.win.blit(sprites.image, offset_rect)
