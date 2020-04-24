import math
import sys
import numpy as np
import arcade
from arcade import Matrix3x3
import random
import os
import timeit


ASPECT_RATIOS = {
    '4:3': 4/3,
    '16:9': 16/9,
    '3:2': 3/2
}
ENGINE_MAPS = {
    'simple test': 0,
    'complex test': 1,
    'wolf3d e1m1': 2
}
'''
vvv COMMONLY ADJUSTED SETTINGS vvv
'''
ENGINE_MAP_NAME = 'simple test'
WINDOW_RES = 240
ASPECT_RATIO = '4:3'
'''
^^^ COMMONLY ADJUSTED SETTINGS ^^^
'''

ENGINE_MAPS_INDEX = ENGINE_MAPS[ENGINE_MAP_NAME]
SCREEN_HEIGHT = WINDOW_RES
SCREEN_WIDTH = int(ASPECT_RATIOS[ASPECT_RATIO] * SCREEN_HEIGHT)

TEX_WIDTH = 64
TEX_HEIGHT = 64

MOVE_SPEED = 5.0
ROTATION_SPEED = 2.0

FLOOR_COLOR = arcade.color.LAWN_GREEN
CEILING_COLOR = arcade.color.DEEP_SKY_BLUE

TEXT_COLOR = arcade.color.BLACK

RENDER_RESOLUTION = 50
TARGET_FPS = 15
TARGET_PLUS_MINUS = 2
MAP_SCALE = 1

MAPS = [np.array([  # simple example map
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]), np.array([  # complex example map
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 7],
    [4, 0, 4, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 7, 7, 0, 7, 7, 7, 7, 7],
    [4, 0, 5, 0, 0, 0, 0, 5, 0, 5, 0, 5, 0, 5, 0, 5, 7, 0, 0, 0, 7, 7, 7, 1],
    [4, 0, 6, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 0, 0, 0, 8],
    [4, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 1],
    [4, 0, 8, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 0, 0, 0, 8],
    [4, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 5, 7, 0, 0, 0, 7, 7, 7, 1],
    [4, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 0, 5, 5, 5, 5, 7, 7, 7, 7, 7, 7, 7, 1],
    [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
    [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
    [4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 6, 0, 6, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 2, 0, 0, 5, 0, 0, 2, 0, 0, 0, 2],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2],
    [4, 0, 6, 0, 6, 0, 0, 0, 0, 4, 6, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 2],
    [4, 0, 0, 5, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2],
    [4, 0, 6, 0, 6, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 5, 0, 0, 2, 0, 0, 0, 2],
    [4, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6, 0, 6, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2],
    [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]
]), np.array([  # Wolfenstein 3D level 1
    [3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3],
    [3, 3, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 3, 0, 3, 3],
    [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
])]

# Wolfenstein 3D level 1


class RaycastingOOP(arcade.Window):
    """
    Main applicaiton class
    """

    def __init__(self, width, height, title, map):
        super().__init__(width, height, title)
        self.min_fps = None  # not in use at the moment
        self.render_resolution = None  # not in use at the moment
        self.max_fps = None  # not in use at the moment
        self.target_fps = None  # not in use at the moment
        self.map_width = None
        self.map_height = None

        self.world_map = map

        self.posX = None
        self.posY = None

        self.dirX = None
        self.dirY = None

        self.planeX = None
        self.planeY = None

        self.fov = None

        self.drawStart = None
        self.drawEnd = None

        self.moveForward = None
        self.moveBackward = None
        self.strafeLeft = None
        self.strafeRight = None
        self.rotateLeft = None
        self.rotateRight = None

        self.time = None
        self.oldTime = None

        self.frameTime = None

        self.move_speed = None
        self.rotation_speed = None

        self.shape_list = None

        self.point_list = None
        self.color_list = None
        self.dark_color_list = None

        self.processing_time = 0
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None

        # self.buffer[SCREEN_HEIGHT][SCREEN_WIDTH] = None  # y-coordinate first because it works per scanline ...?
        self.texture = None
        self.alt_texture = None

        self.xy_square = None

    def setup(self):
        self.map_width = len(self.world_map)
        self.map_height = 0
        for row in self.world_map:
            self.map_height = max(self.map_height, len(row))

        '''
        self.world_map = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 8, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
        ])
        '''

        '''self.point_list = []

        for y in range(len(self.world_map)):
            for x in range(len(self.world_map[y])):
                if self.world_map[x][y] != 0:
                    point = [x, y]
                    while True:
                        try:
                            self.point_list[self.world_map[x][y]].append(point)
                            break
                        except IndexError:
                            self.point_list.append([])'''

        # initialize and declare position variables
        self.posX = 22
        self.posY = 12

        # initialize and declare the look-direction variables
        self.dirX = -1.0
        self.dirY = 0.0

        # initialize and declare the
        self.planeX = 0
        self.planeY = 1

        self.drawStart = []
        self.drawEnd = []

        # initialize and declare movement boolean flags to false
        self.moveForward = False
        self.moveBackward = False
        self.strafeLeft = False
        self.strafeRight = False
        self.rotateLeft = False
        self.rotateRight = False

        # initialize and declare the game time to 0
        self.time = 0

        # start with the default target FPS
        self.target_fps = TARGET_FPS

        # initialize an empty ShapeElementList to store the line objects in
        self.shape_list = arcade.ShapeElementList()
        self.color_list = [
            arcade.color.RED,
            arcade.color.GREEN,
            arcade.color.BLUE,
            arcade.color.WHITE,
            arcade.color.YELLOW,
            arcade.color.PURPLE,
            arcade.color.ORANGE,
            arcade.color.PINK
        ]

        self.dark_color_list = [
            arcade.color.DARK_RED,
            arcade.color.DARK_GREEN,
            arcade.color.DARK_BLUE,
            arcade.color.GRAY,
            arcade.color.DARK_YELLOW,
            arcade.color.DARK_PASTEL_PURPLE,
            arcade.color.DARK_ORANGE,
            arcade.color.DARK_PINK
        ]

        self.render_resolution = RENDER_RESOLUTION

        self.texture = 'bricks.png'
        self.alt_texture = 'darker_bricks.png'

        self.xy_square = arcade.load_texture('bricks.png')

        self.set_exclusive_mouse(exclusive=True)
        self.set_exclusive_keyboard(exclusive=True)

        print(self.world_map)

    def on_draw(self):

        # start timing how long this takes
        draw_start_time = timeit.default_timer()

        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1

        arcade.start_render()

        '''for i, pair in enumerate([
            ['shear(0.0, 0.1)', Matrix3x3().shear(0.0, 0.1)]
        ]):
            x = 80 + 180 * (i % 4)
            y = 420 - (i // 4) * 320
            arcade.draw_text(pair[0], x, y - 20 - pair[0].count('\n') * 10, arcade.color.WHITE, 10)'''
        # self.xy_sqare.draw_transformed(x, y, 100, 100, 0, 250, pair[1])

        '''for color_index in range(len(self.point_list)):
            self.shape_list.append(
                arcade.create_rectangles_filled_with_colors(
                    self.point_list[color_index],
                    self.color_list[color_index]
                )
            )'''

        # draw all shapes in the list
        self.shape_list.draw()

        # draw the target_fps text
        arcade.draw_text(f"Target FPS:\n- <==Q {self.target_fps} E==> +",
                         int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.1),
                         TEXT_COLOR)

        # draw the FPS indicator text
        '''arcade.draw_text(f'FPS: {1.0 / self.frameTime}',
                         int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.9),
                         TEXT_COLOR)'''

        # draw minimap background
        arcade.draw_lrtb_rectangle_filled(0 * MAP_SCALE, 24 * MAP_SCALE, 24 * MAP_SCALE, 0 * MAP_SCALE,
                                          arcade.color.BLACK)

        # draw minimap outer walls
        arcade.draw_lrtb_rectangle_outline(0 * MAP_SCALE, 24 * MAP_SCALE, 24 * MAP_SCALE, 0 * MAP_SCALE,
                                           arcade.color.RED,
                                           MAP_SCALE)

        # draw the player location indicator
        arcade.draw_point((self.posX) * MAP_SCALE, (24 - self.posY) * MAP_SCALE,
                          arcade.color.ORANGE,
                          MAP_SCALE)

        # arcade.draw_line(8*MAP_SCALE,1*MAP_SCALE,1*MAP_SCALE,1*MAP_SCALE,arcade.color.WHITE,MAP_SCALE)
        # arcade.draw_line(1*MAP_SCALE,1*MAP_SCALE,1*MAP_SCALE,7*MAP_SCALE,arcade.color.WHITE,MAP_SCALE)
        '''arcade.draw_line_strip(
            [[8 * MAP_SCALE, 1 * MAP_SCALE],
             [1 * MAP_SCALE, 1 * MAP_SCALE],
             [1 * MAP_SCALE, 7 * MAP_SCALE],
             [3 * MAP_SCALE, 7 * MAP_SCALE],
             [3 * MAP_SCALE, 6 * MAP_SCALE],
             [3 * MAP_SCALE, 7 * MAP_SCALE],
             [8 * MAP_SCALE, 7 * MAP_SCALE],
             [8 * MAP_SCALE, 3 * MAP_SCALE],
             [3 * MAP_SCALE, 3 * MAP_SCALE],
             [3 * MAP_SCALE, 4 * MAP_SCALE]],
            arcade.color.WHITE, MAP_SCALE)
        arcade.draw_line_strip(
            [[6 * MAP_SCALE, 20 * MAP_SCALE],
             [11 * MAP_SCALE, 20 * MAP_SCALE],
             [11 * MAP_SCALE, 15 * MAP_SCALE],
             [6 * MAP_SCALE, 15 * MAP_SCALE],
             [6 * MAP_SCALE, 20 * MAP_SCALE]],
            arcade.color.GREEN,
            MAP_SCALE
        )
        arcade.draw_points(
            [[16 * MAP_SCALE, 20 * MAP_SCALE],
             [18 * MAP_SCALE, 20 * MAP_SCALE],
             [20 * MAP_SCALE, 20 * MAP_SCALE],
             [20 * MAP_SCALE, 18 * MAP_SCALE],
             [20 * MAP_SCALE, 16 * MAP_SCALE],
             [18 * MAP_SCALE, 16 * MAP_SCALE],
             [16 * MAP_SCALE, 16 * MAP_SCALE],
             [16 * MAP_SCALE, 18 * MAP_SCALE]],
            arcade.color.BLUE,
            MAP_SCALE
        )

        arcade.draw_point(6 * MAP_SCALE, 5 * MAP_SCALE,
                          arcade.color.YELLOW,
                          MAP_SCALE)'''

        # display timings
        output = f'Processing time: {self.processing_time:.3f}'
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 20, arcade.color.BLACK, 16)

        output = f'Drawing time: {self.draw_time:.3f}'
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.BLACK, 16)

        if self.fps is not None:
            output = f'FPS: {self.fps:.0f}'
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 60, arcade.color.BLACK, 16)

        self.draw_time = timeit.default_timer() - draw_start_time

    def on_update(self, delta_time):

        self.max_fps = self.target_fps + TARGET_PLUS_MINUS
        self.min_fps = self.target_fps - TARGET_PLUS_MINUS

        self.shape_list = arcade.ShapeElementList()

        '''floor = arcade.create_rectangle(
            SCREEN_WIDTH // 0, int(SCREEN_HEIGHT * 0.25),
            SCREEN_WIDTH, SCREEN_HEIGHT // 0,
            FLOOR_COLOR
        )

        ceiling = arcade.create_rectangle(
            SCREEN_WIDTH // 0, int(SCREEN_HEIGHT * 0.75),
            SCREEN_WIDTH, SCREEN_HEIGHT // 0,
            CEILING_COLOR
        )

        self.shape_list.append(floor)
        self.shape_list.append(ceiling)'''

        point_list = []
        color_list = []

        # print(f'({self.posX}, {self.posY}) at time {self.time}')

        # arcade.start_render()
        for x in range(0, SCREEN_WIDTH + 1):
            # calculate the ray position and direction
            cameraX = (2 * x / SCREEN_WIDTH) - 1
            if cameraX > 1 or cameraX < -1:
                print('cameraX is too big or too small!')
                sys.exit()
            rayDirX = self.dirX + self.planeX * cameraX
            rayDirY = self.dirY + self.planeY * cameraX

            # which box of the map we're in
            mapX = int(self.posX)
            mapY = int(self.posY)

            # print(f'({mapX}, {mapY})')

            # length of ray from current position to the next x- or y-side
            sideDistX = None
            sideDistY = None

            # length of the ray from one x- or y-side to the next x- or y-side
            try:
                deltaDistX = abs(1 / rayDirX)
            except ZeroDivisionError:
                if rayDirY == 0:
                    deltaDistX = 0
                else:
                    if rayDirX == 0:
                        deltaDistX = 1
                    else:
                        deltaDistX = abs(1 / rayDirX)
            try:
                deltaDistY = abs(1 / rayDirY)
            except ZeroDivisionError:
                if rayDirX == 0:
                    deltaDistY = 0
                else:
                    if rayDirY == 0:
                        deltaDistY = 1
                    else:
                        deltaDistY = abs(1 / rayDirY)
            perpWallDist = None

            # which direction to step in the x direction or y direction (either +1 or -1)
            stepX = None
            stepY = None

            hit = 0  # was there a wall hit?
            side = None  # was a North/South wall hit or an East/West wall hit?
            if rayDirX < 0:
                stepX = -1
                sideDistX = (self.posX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - self.posX) * deltaDistX

            if rayDirY < 0:
                stepY = -1
                sideDistY = (self.posY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - self.posY) * deltaDistY

            # was a wall hit? 1 = yes. 0 = no.
            while hit == 0:
                if sideDistX < sideDistY:
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                # check if ray has hit a wall
                if self.world_map[mapX][mapY] > 0:
                    hit = 1

            if side == 0:
                perpWallDist = (mapX - self.posX + (1 - stepX) / 2) / (rayDirX + 0.00000001)
            else:
                perpWallDist = (mapY - self.posY + (1 - stepY) / 2) / (rayDirY + 0.00000001)

            lineHeight = int(SCREEN_HEIGHT / (perpWallDist + 0.00000001))

            drawStart = -lineHeight / 2 + SCREEN_HEIGHT / 2
            if drawStart < 0:
                drawStart = 0

            drawEnd = lineHeight / 2 + SCREEN_HEIGHT / 2
            if drawEnd >= SCREEN_HEIGHT:
                drawEnd = SCREEN_HEIGHT - 1

            # texturing calculations
            tex_num = self.world_map[mapX][mapY] - 1  # 1 subtracted from it so that texture 0 acn be used!

            # calculate value of wallX
            wallX = None  # where exactly the wall was hit
            if side == 0:
                wallX = self.posY + perpWallDist * rayDirY
            else:
                wallX = self.posX + perpWallDist * rayDirX

            wallX -= math.floor(wallX)

            # x coordinate on the texture
            texX = int(wallX * TEX_WIDTH)
            if side == 0 and rayDirX > 0:
                texX = TEX_WIDTH - texX - 1
            if side == 1 and rayDirY < 0:
                texX = TEX_WIDTH - texX - 1

            if side == 0:
                try:
                    color = self.color_list[self.world_map[mapX][mapY]]
                except IndexError:
                    color = arcade.color.YELLOW
            elif side == 1:
                try:
                    color = self.dark_color_list[self.world_map[mapX][mapY]]
                except IndexError:
                    color = arcade.color.DARK_YELLOW

            '''# how much to increase the texture coordinate per screen pixel
            step = 1.0 * TEX_HEIGHT / lineHeight
            tex_pos = (drawStart - SCREEN_HEIGHT / 2 + lineHeight / 2) * step
            for y in range(drawStart, drawEnd):
                texY = int(tex_pos)
                tex_pos += step

                if side == 1:
                    tex_to_use = self.alt_texture
                else:
                    tex_to_use = self.texture'''

            draw_start_pos = (x, drawStart)
            draw_end_pos = (x, drawEnd)
            point_list.append(draw_end_pos)
            point_list.append(draw_start_pos)
            for i in range(2):
                color_list.append(color)

            # self.shape_list.append(arcade.create_line(x, drawStart, x, drawEnd, color, self.render_resolution))
        shape = arcade.create_line_generic_with_colors(point_list, color_list, 0, 1)
        self.shape_list.append(shape)

        self.oldTime = self.time
        self.time += delta_time

        self.frameTime = (self.time - self.oldTime)  # frameTime is the time this frame has taken in seconds
        # print(1.0 / self.frameTime)  # FPS counter
        FPS = 1 / self.frameTime
        if FPS < self.min_fps:
            self.render_resolution += 1
        elif FPS > self.max_fps:
            self.render_resolution -= 1
        self.move_speed = self.frameTime * MOVE_SPEED  # constant value in squares/second
        self.rotation_speed = self.frameTime * ROTATION_SPEED  # constant value in radians/second

        print(self.rotation_speed)

        if self.moveForward:
            if not self.world_map[int(self.posX + self.dirX * self.move_speed)][int(self.posY)]:
                self.posX += self.dirX * self.move_speed
            if not self.world_map[int(self.posX)][int(self.posY + self.dirY * self.move_speed)]:
                self.posY += self.dirY * self.move_speed
        elif self.moveBackward:
            if not self.world_map[int(self.posX - self.dirX * self.move_speed)][int(self.posY)]:
                self.posX -= self.dirX * self.move_speed
            if not self.world_map[int(self.posX)][int(self.posY - self.dirY * self.move_speed)]:
                self.posY -= self.dirY * self.move_speed

        if self.strafeLeft:
            if not self.world_map[int(self.posX - self.dirY * self.move_speed)][int(self.posY)]:
                self.posX -= self.dirY * self.move_speed
            if not self.world_map[int(self.posX)][int(self.posY + self.dirX * self.move_speed)]:
                self.posY += self.dirX * self.move_speed
        elif self.strafeRight:
            if not self.world_map[int(self.posX + self.dirY * self.move_speed)][int(self.posY)]:
                self.posX += self.dirY * self.move_speed
            if not self.world_map[int(self.posX)][int(self.posY - self.dirX * self.move_speed)]:
                self.posY -= self.dirX * self.move_speed

        if self.rotateLeft:
            # both camera direction and camera plane must be rotated
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(self.rotation_speed) - self.dirY * math.sin(self.rotation_speed)
            self.dirY = oldDirX * math.sin(self.rotation_speed) + self.dirY * math.cos(self.rotation_speed)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(self.rotation_speed) - self.planeY * math.sin(self.rotation_speed)
            self.planeY = oldPlaneX * math.sin(self.rotation_speed) + self.planeY * math.cos(self.rotation_speed)
        elif self.rotateRight:
            # both camera direction and camera plane must be rotated
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(-self.rotation_speed) - self.dirY * math.sin(-self.rotation_speed)
            self.dirY = oldDirX * math.sin(-self.rotation_speed) + self.dirY * math.cos(-self.rotation_speed)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(-self.rotation_speed) - self.planeY * math.sin(-self.rotation_speed)
            self.planeY = oldPlaneX * math.sin(-self.rotation_speed) + self.planeY * math.cos(-self.rotation_speed)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            # print('W/UP')
            self.moveForward = True
        if key == arcade.key.A:
            # print('A/LEFT')
            self.strafeLeft = True
        if key == arcade.key.S:
            # print('S/DOWN')
            self.moveBackward = True
        if key == arcade.key.D:
            # print('D/RIGHT')
            self.strafeRight = True
        if key == arcade.key.LEFT:
            self.rotateLeft = True
        if key == arcade.key.RIGHT:
            self.rotateRight = True
        if key == arcade.key.Q:
            self.target_fps -= 1
        if key == arcade.key.E:
            self.target_fps += 1
        if key == arcade.key.ESCAPE:
            sys.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.moveForward = False
        if key == arcade.key.S:
            self.moveBackward = False
        if key == arcade.key.A:
            self.strafeLeft = False
        if key == arcade.key.D:
            self.strafeRight = False
        if key == arcade.key.LEFT:
            self.rotateLeft = False
        if key == arcade.key.RIGHT:
            self.rotateRight = False

    def generate_minimap(self):
        pass


def main():
    game = RaycastingOOP(SCREEN_WIDTH, SCREEN_HEIGHT, "Raycasting in Python", MAPS[ENGINE_MAPS_INDEX])
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
