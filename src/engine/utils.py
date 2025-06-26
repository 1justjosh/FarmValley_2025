from src.engine.settings import *

def load_tile_map(path,tile_width,tile_height,*args,**kwargs):
    base_image = pg.image.load(path).convert_alpha()
    images = []

    for y in range(int(base_image.get_height() // tile_height)):
        for x in range(int(base_image.get_width() // tile_width)):
            temp_image = base_image.subsurface((x * tile_width, y * tile_height,tile_width,tile_height))
            if kwargs.get("scale",False):
                temp_image = pg.transform.scale(temp_image,kwargs["scale"])
            images.append(temp_image)

    return images

def get_joystick_pressed(joystick,number):
    if not joystick:
        return False

    return joystick.get_button(number)

def get_joystick_axis(joystick, axis_num, deadzone=0.8):
    if not joystick:
        return 0

    value = joystick.get_axis(axis_num)
    return value if abs(value) > deadzone else 0