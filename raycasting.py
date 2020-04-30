import math
import sys

import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

MOVE_SPEED = 5.0
ROTATION_SPEED = 2.0


class RaycastingEngine(arcade.Window):
    """
    This class creates an arcade window subclass, RaycastingEngine, meant for first-person games
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        # level map
        self.map = None

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

        # gameplay
        self.move_speed = None
        self.rotation_speed = None
        self.constant_move_speed = None
        self.constant_rotation_speed = None

    def setup(self,
              player_start: tuple,
              look_start: tuple,
              plane_start: tuple,
              level_map,
              player_move_speed=MOVE_SPEED,
              player_rotation_speed=ROTATION_SPEED,
              floor_color=arcade.color.BLACK,
              ceiling_color=arcade.color.BLACK,
              strafe_enabled=True,
              hide_mouse=True):

        # level map
        self.map = level_map

        # player parameters
        self.pos_x = player_start[0]
        self.pos_y = player_start[1]

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
            self.set_exclusive_mouse(exclusive=True)

        # gameplay
        self.constant_move_speed = player_move_speed
        self.constant_rotation_speed = player_rotation_speed

    def on_update(self, delta_time):
        # clear the shape list for the new frame
        self.shape_list = arcade.ShapeElementList()

        # set the floor and ceiling colors
        floor = arcade.create_rectangle(
            SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.25),
            SCREEN_WIDTH, SCREEN_HEIGHT // 2,
            self.floor_color
        )

        ceiling = arcade.create_rectangle(
            SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.75),
            SCREEN_WIDTH, SCREEN_HEIGHT // 2,
            self.ceiling_color
        )

        # add the floor and ceiling shapes to the shape_list
        self.shape_list.append(floor)
        self.shape_list.append(ceiling)

        # create the point_list and color_list for raycasting
        point_list = []
        color_list = []

        # begin raycasting
        for x in range(0, SCREEN_WIDTH + 1):
            # calculate the ray position and direction
            camera_x = (2 * x / SCREEN_WIDTH) - 1
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
                if self.map[map_x][map_y] > 0:
                    hit = 1

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
            line_height = int(SCREEN_HEIGHT / (perpendicular_wall_dist + 0.00000001))

            # the pixel (height) at which to start drawing the wall
            draw_start = -line_height / 2 + SCREEN_HEIGHT / 2

            if draw_start < 0:
                draw_start = 0

            draw_end = line_height / 2 + SCREEN_HEIGHT / 2
            if draw_end >= SCREEN_HEIGHT:
                draw_end = SCREEN_HEIGHT - 1

            # set the color with which to draw the given pixel column
            if side == 0:
                try:
                    color = self.main_wall_color_list[self.map[map_x][map_y]]
                except IndexError:
                    color = arcade.color.YELLOW
            elif side == 1:
                try:
                    color = self.dark_wall_color_list[self.map[map_x][map_y]]
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

    def on_draw(self):

        arcade.start_render()

        # draw all the shapes in the list
        self.shape_list.draw()

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


def pick_map(map_number: int):
    maps = [
        [  # simple example map
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
        ]
    ]
    return maps[map_number]


def main():
    raycasting = RaycastingEngine(SCREEN_WIDTH, SCREEN_HEIGHT, "Raycasting Engine")
    raycasting.setup((22, 12), (-1, 0), (0, 0.66), pick_map(1), )

    arcade.run()


if __name__ == "__main__":
    main()
else:
    pass
