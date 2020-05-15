import math
import sys
import worldmap as wm
import minimap as mm
import arcade
import pyautogui
import copy

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVE_SPEED = 5.0
ROTATION_SPEED = 2.0

MINIMAP_POS_X = 10
MINIMAP_POS_Y = 30

MINIMAP_SIZE = 2


class RaycastingEngine(arcade.Window):
    """
    This class creates an arcade view subclass, RaycastingEngine, meant for first-person games
    """

    def __init__(self, width, height, title, fullscreen=True):
        super().__init__(width, height, title, fullscreen=fullscreen)

        # set the window to fullscreen by default

        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

        # save the window size so we can reference it later
        self.screen_width, self.screen_height = self.get_size()

        # level map
        self.map = None
        self.minimap = None
        self.mm_bg_points = None
        self.mm_bg_colors = None
        self.mm_point_list = None
        self.mm_color_list = None

        # player parameters
        self.pos_x = None
        self.pos_y = None

        self.dir_x = None
        self.dir_y = None

        self.plane_x = None
        self.plane_y = None

        # movement boolean flags
        self.move_forward = None
        self.move_backward = None
        self.strafe_left = None
        self.strafe_right = None
        self.rotate_left = None
        self.rotate_right = None

        self.mouse_look = None
        self.last_x = None
        self.last_y = None  # currently no implementation for this, just a placeholder
        self.rotate_x_magnitude = None
        self.rotate_y_magnitude = None  # currently no implementation for this, just a placeholder

        self.mouse_deadzone = None

        self.last_frame = None

        # performance statistics
        self.time = None
        self.old_time = None

        # drawing
        self.shape_list = None
        self.point_list = None
        self.main_wall_color_list = None
        self.dark_wall_color_list = None
        self.floor_color = None
        self.ceiling_color = None
        self.minimap = None

        # gameplay
        self.move_speed = None
        self.rotation_speed = None
        self.constant_move_speed = None
        self.constant_rotation_speed = None

    def setup(self, player_start: tuple, look_start: tuple, plane_start: tuple, level_map, player_move_speed=MOVE_SPEED,
              player_rotation_speed=ROTATION_SPEED, floor_color=arcade.color.BLACK, ceiling_color=arcade.color.BLACK,
              strafe_enabled=True, hide_mouse=True, mouse_look=False):

        # level map
        self.map = level_map
        self.minimap = []

        for i in range(len(self.map)):
            self.minimap.append([])
            for j in range(len(self.map[i])):
                if i == 0 or j == 0 or i == len(self.map) - 1 or j == len(self.map[i]) - 1:
                    self.minimap.append(True)
                else:
                    self.minimap.append(False)

        self.mm_bg_points = [
            # top-left
            (MINIMAP_POS_X, MINIMAP_POS_Y + len(self.minimap) * MINIMAP_SIZE),
            # top-right
            (MINIMAP_POS_X + len(self.minimap[0]) * MINIMAP_SIZE, MINIMAP_POS_Y + len(self.minimap) * MINIMAP_SIZE),
            # bottom-right
            (MINIMAP_POS_X + len(self.minimap[0]) * MINIMAP_SIZE, MINIMAP_POS_Y),
            # bottom-left
            (MINIMAP_POS_X, MINIMAP_POS_Y)
        ]
        self.mm_bg_colors = []
        for i in range(4):
            self.mm_bg_colors.append(arcade.color.LAWN_GREEN)

        self.mm_point_list = []
        self.mm_color_list = []

        # player parameters
        self.pos_x = player_start[0]
        self.pos_y = player_start[1]

        # if the player is not starting in an open space, start searching from the top left of the list for
        # an open space
        if self.map[self.pos_y][self.pos_x] != 0:
            for i in range(len(self.map)):
                for j in range(len(self.map[i])):
                    if self.map[i][j] == 0:
                        self.pos_x = j
                        self.pos_y = i
                        break

        self.dir_x = look_start[0]
        self.dir_y = look_start[1]

        self.plane_x = plane_start[0]
        self.plane_y = plane_start[1]

        # movement boolean flags
        self.move_forward = False
        self.move_backward = False
        if strafe_enabled:
            self.strafe_left = False
            self.strafe_right = False
        self.rotate_left = False
        self.rotate_right = False

        self.mouse_look = mouse_look
        self.last_x = self.screen_width // 2
        self.last_y = self.screen_height // 2
        self.rotate_x_magnitude = 1
        self.rotate_y_magnitude = 1

        self.last_frame = []

        # performance statistics
        self.time = 0
        self.old_time = 0

        # drawing
        self.shape_list = arcade.ShapeElementList()

        self.main_wall_color_list = [
            arcade.color.RED,
            arcade.color.GREEN,
            arcade.color.BLUE,
            arcade.color.WHITE,
            arcade.color.YELLOW,
            arcade.color.PURPLE,
            arcade.color.ORANGE,
            arcade.color.PINK
        ]

        self.dark_wall_color_list = [
            arcade.color.DARK_RED,
            arcade.color.DARK_GREEN,
            arcade.color.DARK_BLUE,
            arcade.color.GRAY,
            arcade.color.DARK_YELLOW,
            arcade.color.DARK_PASTEL_PURPLE,
            arcade.color.DARK_ORANGE,
            arcade.color.DARK_PINK
        ]

        self.floor_color = floor_color

        self.ceiling_color = ceiling_color

        # hide the mouse by default
        if hide_mouse:
            self.set_mouse_visible(False)
            self.set_exclusive_mouse(exclusive=True)
        else:
            self.set_mouse_visible(True)

        self.mouse_deadzone = 0

        self.minimap = []
        for i in range(len(self.map)):
            self.minimap.append([])
            for j in range(len(self.map[i])):
                self.minimap[i].append(None)

        # gameplay
        self.constant_move_speed = player_move_speed
        self.constant_rotation_speed = player_rotation_speed

    def on_update(self, delta_time):
        # clear the shape list for the new frame
        self.shape_list = arcade.ShapeElementList()
        # self.minimap_shape_list = arcade.ShapeElementList()

        # set the floor and ceiling colors
        floor = arcade.create_rectangle(
            self.screen_width // 2, int(self.screen_height * 0.25),
            self.screen_width, self.screen_height // 2,
            self.floor_color
        )

        ceiling = arcade.create_rectangle(
            self.screen_width // 2, int(self.screen_height * 0.75),
            self.screen_width, self.screen_height // 2,
            self.ceiling_color
        )

        # add the floor and ceiling shapes to the shape_list
        self.shape_list.append(floor)
        self.shape_list.append(ceiling)

        # create the point_list and color_list for raycasting
        point_list = []
        color_list = []

        # begin raycasting
        for x in range(0, self.screen_width + 1):
            # calculate the ray position and direction
            camera_x = (2 * x / self.screen_width) - 1
            if camera_x > 1 or camera_x < -1:
                print('camera_x is too big or too small!')
                print(f'camera_x = {camera_x}')
            ray_dir_x = self.dir_x + self.plane_x * camera_x
            ray_dir_y = self.dir_y + self.plane_y * camera_x

            # determine which grid-square of the map we're in
            map_x = int(self.pos_x)
            map_y = int(self.pos_y)

            # length of ray from the current position to the next vertical gridline
            side_dist_x = None
            # length of ray from the current position to the next horizontal gridline
            side_dist_y = None

            # length of the ray from one horizontal or vertical gridline to the next one
            try:
                delta_dist_x = abs(1 / ray_dir_x)
            except ZeroDivisionError:
                if ray_dir_y == 0:
                    delta_dist_x = 0
                elif ray_dir_x == 0:
                    delta_dist_x = 1
                else:
                    delta_dist_x = abs(1 / ray_dir_x)

            try:
                delta_dist_y = abs(1 / ray_dir_y)
            except ZeroDivisionError:
                if ray_dir_x == 0:
                    delta_dist_y = 0
                elif ray_dir_y == 0:
                    delta_dist_y = 1
                else:
                    delta_dist_y = abs(1 / ray_dir_y)

            # the distance to the next perpendicular wall
            perpendicular_wall_dist = None

            # which direction to step in the x direction or the y direction (either +1 or -1)
            step_x = None
            step_y = None

            # was a there a wall hit?
            hit = 0

            # was a North/South wall hit or an East/West wall hit?
            side = None

            if ray_dir_x < 0:
                step_x = -1
                side_dist_x = (self.pos_x - map_x) * delta_dist_x
            else:
                step_x = 1
                side_dist_x = (map_x + 1 - self.pos_x) * delta_dist_x

            if ray_dir_y < 0:
                step_y = -1
                side_dist_y = (self.pos_y - map_y) * delta_dist_y
            else:
                step_y = 1
                side_dist_y = (map_y + 1 - self.pos_y) * delta_dist_y

            # continually cast the ray out into the distance until it hits a wall
            while hit == 0:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                # check if the ray has hit a wall yet
                if 0 < self.map[map_x][map_y] < 10:
                    hit = 1
                    if not self.minimap[map_x][map_y]:
                        self.minimap[map_x][map_y] = True
                        # top-left
                        self.mm_point_list.append(
                            (MINIMAP_POS_X + map_x * MINIMAP_SIZE, MINIMAP_POS_Y + map_y * MINIMAP_SIZE + MINIMAP_SIZE))
                        self.mm_color_list.append(arcade.color.BLACK)
                        # top-right
                        self.mm_point_list.append((MINIMAP_POS_X + map_x * MINIMAP_SIZE + MINIMAP_SIZE,
                                                   MINIMAP_POS_Y + map_y * MINIMAP_SIZE + MINIMAP_SIZE))
                        self.mm_color_list.append(arcade.color.BLACK)
                        # bottom-right
                        self.mm_point_list.append(
                            (MINIMAP_POS_X + map_x * MINIMAP_SIZE + MINIMAP_SIZE, MINIMAP_POS_Y + map_y * MINIMAP_SIZE))
                        self.mm_color_list.append(arcade.color.BLACK)
                        # bottom-left
                        self.mm_point_list.append(
                            (MINIMAP_POS_X + map_x * MINIMAP_SIZE, MINIMAP_POS_Y + map_y * MINIMAP_SIZE))
                        self.mm_color_list.append(arcade.color.BLACK)
                elif 10 <= self.map[map_x][map_y] < 20:
                    hit = 2

            if side == 0:
                perpendicular_wall_dist = (map_x - self.pos_x + (1 - step_x) / 2) / (ray_dir_x + 0.00000001)
            else:
                perpendicular_wall_dist = (map_y - self.pos_y + (1 - step_y) / 2) / (ray_dir_y + 0.00000001)

            """
            **********************************************
            MODIFY CODE BELOW FOR ALLOWING PITS/HIGH WALLS
            **********************************************
            """

            # the height of the wall at the given pixel column
            line_height = int(self.screen_height / (perpendicular_wall_dist + 0.00000001))

            # the pixel (height) at which to start drawing the wall
            draw_start = -line_height / 2 + self.screen_height / 2

            if draw_start < 0:
                draw_start = 0

            if hit == 1:  # if the wall is single-height
                draw_end = line_height / 2 + self.screen_height / 2
            elif hit == 2:  # otherwise, if the wall is double-height
                draw_end = line_height + self.screen_height / 2
            if draw_end >= self.screen_height:
                draw_end = self.screen_height - 1

            # set the color with which to draw the given pixel column
            if side == 0:
                try:
                    color = self.main_wall_color_list[self.map[map_x][map_y] % 10]
                except IndexError:
                    color = arcade.color.YELLOW
            elif side == 1:
                try:
                    color = self.dark_wall_color_list[self.map[map_x][map_y] % 10]
                except IndexError:
                    color = arcade.color.DARK_YELLOW

            draw_start_pos = (x, draw_start)
            draw_end_pos = (x, draw_end)
            point_list.append(draw_start_pos)
            point_list.append(draw_end_pos)
            for i in range(2):
                color_list.append(color)

        shape = arcade.create_line_generic_with_colors(point_list, color_list, 3)
        self.shape_list.append(shape)

        minimap_background = arcade.create_rectangle_filled_with_colors(self.mm_bg_points, self.mm_bg_colors)
        self.shape_list.append(minimap_background)

        minimap_shape = arcade.create_rectangles_filled_with_colors(self.mm_point_list, self.mm_color_list)
        self.shape_list.append(minimap_shape)

        ppos_point_list = []
        ppos_color_list = []

        # top-left
        ppos_point_list.append(
            (MINIMAP_POS_X + self.pos_x * MINIMAP_SIZE, MINIMAP_POS_Y + self.pos_y * MINIMAP_SIZE + MINIMAP_SIZE))
        ppos_color_list.append(arcade.color.BLUE)
        # top-right
        ppos_point_list.append((MINIMAP_POS_X + self.pos_x * MINIMAP_SIZE + MINIMAP_SIZE,
                                MINIMAP_POS_Y + self.pos_y * MINIMAP_SIZE + MINIMAP_SIZE))
        ppos_color_list.append(arcade.color.RED)
        # bottom-right
        ppos_point_list.append(
            (MINIMAP_POS_X + self.pos_x * MINIMAP_SIZE + MINIMAP_SIZE, MINIMAP_POS_Y + self.pos_y * MINIMAP_SIZE))
        ppos_color_list.append(arcade.color.BLUE)
        # bottom-left
        ppos_point_list.append((MINIMAP_POS_X + self.pos_x * MINIMAP_SIZE, MINIMAP_POS_Y + self.pos_y * MINIMAP_SIZE))
        ppos_color_list.append(arcade.color.BLUE)

        player_shape = arcade.create_rectangle_filled_with_colors(ppos_point_list, ppos_color_list)
        self.shape_list.append(player_shape)

        self.old_time = self.time
        self.time += delta_time

        # frame_time is the amount of time this frame spent on screen (in seconds)
        frame_time = (self.time - self.old_time)

        FPS = 1 / frame_time
        """
        ********************************************************
        HERE IS WHERE THE CODE FOR AUTO QUALITY ADJUST SHOULD GO
        ********************************************************
        """

        self.move_speed = frame_time * self.constant_move_speed
        self.rotation_speed = frame_time * self.constant_rotation_speed
        # print(f'constant rotation speed: {self.constant_rotation_speed}\nframe time: {frame_time}\nadjusted rotation speed: {self.rotation_speed}')
        self.rotation_speed *= (self.rotate_x_magnitude / 100)

        if self.move_forward:
            if not self.map[int(self.pos_x + self.dir_x * self.move_speed)][int(self.pos_y)]:
                self.pos_x += self.dir_x * self.move_speed
            if not self.map[int(self.pos_x)][int(self.pos_y + self.dir_y * self.move_speed)]:
                self.pos_y += self.dir_y * self.move_speed
        elif self.move_backward:
            if not self.map[int(self.pos_x - self.dir_x * self.move_speed)][int(self.pos_y)]:
                self.pos_x -= self.dir_x * self.move_speed
            if not self.map[int(self.pos_x)][int(self.pos_y - self.dir_y * self.move_speed)]:
                self.pos_y -= self.dir_y * self.move_speed

        if self.strafe_left:
            if not self.map[int(self.pos_x - self.dir_y * self.move_speed)][int(self.pos_y)]:
                self.pos_x -= self.dir_y * self.move_speed
            if not self.map[int(self.pos_x)][int(self.pos_y + self.dir_x * self.move_speed)]:
                self.pos_y += self.dir_x * self.move_speed
        elif self.strafe_right:
            if not self.map[int(self.pos_x + self.dir_y * self.move_speed)][int(self.pos_y)]:
                self.pos_x += self.dir_y * self.move_speed
            if not self.map[int(self.pos_x)][int(self.pos_y - self.dir_x * self.move_speed)]:
                self.pos_y -= self.dir_x * self.move_speed

        if self.rotate_left:
            # both camera direction and camera plane must be rotated
            old_dir_x = self.dir_x
            self.dir_x = self.dir_x * math.cos(self.rotation_speed) - self.dir_y * math.sin(self.rotation_speed)
            self.dir_y = old_dir_x * math.sin(self.rotation_speed) + self.dir_y * math.cos(self.rotation_speed)
            old_plane_x = self.plane_x
            self.plane_x = self.plane_x * math.cos(self.rotation_speed) - self.plane_y * math.sin(self.rotation_speed)
            self.plane_y = old_plane_x * math.sin(self.rotation_speed) + self.plane_y * math.cos(self.rotation_speed)
        elif self.rotate_right:
            # both camera direction and camera plane must be rotated
            old_dir_x = self.dir_x
            self.dir_x = self.dir_x * math.cos(-self.rotation_speed) - self.dir_y * math.sin(-self.rotation_speed)
            self.dir_y = old_dir_x * math.sin(-self.rotation_speed) + self.dir_y * math.cos(-self.rotation_speed)
            old_plane_x = self.plane_x
            self.plane_x = self.plane_x * math.cos(-self.rotation_speed) - self.plane_y * math.sin(-self.rotation_speed)
            self.plane_y = old_plane_x * math.sin(-self.rotation_speed) + self.plane_y * math.cos(-self.rotation_speed)
        if self.mouse_look:
            self.mouse_look = False
            self.rotate_right = False
            self.rotate_left = False

    def on_draw(self):

        arcade.start_render()
        self.shape_list.draw()

        arcade.draw_text(
            "Mouse deadzone increase: UP\nMouse deadzone decrease: DOWN\nMouse sensitivity incerase: +\nMouse sensitivity decrease: -",
            0, 0, color=arcade.color.BLACK)

        """
        ********************************
        INSERT MINIMAP DRAWING CODE HERE
        ********************************
        """

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.move_forward = True
        if key == arcade.key.A:
            self.strafe_left = True
        if key == arcade.key.S:
            self.move_backward = True
        if key == arcade.key.D:
            self.strafe_right = True
        if key == arcade.key.LEFT:
            self.rotate_left = True
        if key == arcade.key.RIGHT:
            self.rotate_right = True
        if key == arcade.key.ESCAPE:
            sys.exit()

        if key == arcade.key.UP:
            self.mouse_deadzone += 1
        elif key == arcade.key.DOWN and self.mouse_deadzone > 0:
            self.mouse_deadzone -= 1

        if key == arcade.key.EQUAL:
            self.constant_rotation_speed += 0.5
        elif key == arcade.key.MINUS and self.constant_rotation_speed >= 1:
            self.constant_rotation_speed -= 0.5

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.move_forward = False
        if key == arcade.key.A:
            self.strafe_left = False
        if key == arcade.key.S:
            self.move_backward = False
        if key == arcade.key.D:
            self.strafe_right = False
        if key == arcade.key.LEFT:
            self.rotate_left = False
        if key == arcade.key.RIGHT:
            self.rotate_right = False

    def on_mouse_motion(self, x, y, dx, dy):
        # pyautogui.moveTo(self.screen_width//2, self.screen_height//2)
        self.mouse_look = True
        if dx > self.mouse_deadzone:
            self.rotate_right = True
            self.rotate_x_magnitude = abs(dx)
            # print(self.rotate_x_magnitude)
        elif dx < -self.mouse_deadzone:
            self.rotate_left = True
            self.rotate_x_magnitude = abs(dx)
            # print(self.rotate_x_magnitude)

        self.last_x = x

    def on_mouse_press(self, x, y, button, modifiers):
        print(f'press: {button} @ ({x}, {y})')


class MenuView(arcade.View):

    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Paused")


def pick_map(map_number: int):
    maps = [
        [  # simple example map
            [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11],
            [11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]
        ],
        [  # complex example map
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
        ],
    ]
    return maps[map_number]


def main():
    world_map_test = wm.Maze(30, 30)
    world_map_test.generate_with_recursive_backtracking(0, 0)
    # print(world_map_test)
    raycasting = RaycastingEngine(SCREEN_WIDTH, SCREEN_HEIGHT, "Raycasting Engine", fullscreen=True)
    raycasting.setup((0, 0), (-1, 0), (0, 0.66), world_map_test.get_map_for_raycasting(), hide_mouse=True,
                     floor_color=arcade.color.LAWN_GREEN, ceiling_color=arcade.color.DEEP_SKY_BLUE)

    arcade.run()

    while True:
        mouse_x, mouse_y = pyautogui.position()

        if mouse_x == raycasting.screen_width - 1:
            pyautogui.moveTo(0, mouse_y)
        elif mouse_x == 0:
            pyautogui.moveTo(raycasting.screen_width - 1, mouse_y)


if __name__ == "__main__":
    main()
else:
    pass
