import os

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
FPS = 60
TITLE = "Pigeonhole"

TILE_WIDTH = 64
TILE_HEIGHT = TILE_WIDTH
TILE_SIZE = TILE_WIDTH, TILE_HEIGHT

SIDEBAR_WIDTH = 330
LEVEL_RECTANGLE = (SIDEBAR_WIDTH,
                   0,
                   WINDOW_WIDTH - SIDEBAR_WIDTH,
                   WINDOW_HEIGHT)
LEVEL_RECTANGLE_CENTER = (LEVEL_RECTANGLE[0] + LEVEL_RECTANGLE[2]//2,
                          LEVEL_RECTANGLE[1] + LEVEL_RECTANGLE[3]//2)

SIDEBAR_HEIGHT = WINDOW_HEIGHT
SIDEBAR_RECT = (0, 0, SIDEBAR_WIDTH, SIDEBAR_HEIGHT)

CARD_WIDTH = 140
CARD_HEIGHT = 220
CARD_SIZE = CARD_WIDTH, CARD_HEIGHT

CHARS_PER_SECOND = 40


def image_path(rel):
    return os.path.join("assets", "images", rel)


def level_path(rel):
    return os.path.join("assets", "levels", rel)


def font_path(rel):
    return os.path.join("assets", "fonts", rel)


def sound_path(rel):
    return os.path.join("assets", "sounds", rel)
