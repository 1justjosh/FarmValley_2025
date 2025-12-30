from enum import StrEnum, IntEnum

class ResourceType(StrEnum):
    BIG_LOG = "big-log"
    SMALL_LOG = "small-log"

    STICK = "stick"
    BRANCH = "branch"

    WOOD_PLANK = "wood-plank"

    STONE = "stone"
    PEBBLE = "pebble"
    IRON_INGOT = "iron-ingot"

    LEAVES = "leaves"

class ToolType(StrEnum):
    WATERING_CAN = "watering-can"
    AXE = "axe"
    HOE = "how"
