import math
import sys
import numpy as np

import calculations as calc
import arcade

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 360

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


class RaycastingOOP(arcade.Window):
    """
    Main applicaiton class
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.min_fps = None
        self.render_resolution = None
        self.max_fps = None
        self.target_fps = None
        self.map_width = None
        self.map_height = None

        self.world_map = None

        self.posX = None
        self.posY = None
        self.pos = None

        self.dirX = None
        self.dirY = None
        self.dir = None

        self.planeX = None
        self.planeY = None
        self.plane = None

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

        self.rotation_matrix = None

    def setup(self):
        self.map_width = 24
        self.map_height = 24

        self.world_map = np.array([
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
        ])

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
        self.pos = np.array([22,  12])

        # initialize and declare the look-direction variables
        self.dirX = -1.0
        self.dirY = 0.0
        self.dir = np.array([-1.0, 0.0])

        # initialize and declare the
        self.planeX = 0
        self.planeY = 0.66
        self.plane = np.array([0, 0.66])

        self.drawStart = np.empty(SCREEN_WIDTH)
        self.drawEnd = np.empty(SCREEN_WIDTH)

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

    def on_draw(self):
        arcade.start_render()

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
        arcade.draw_text(f'FPS: {1.0 / self.frameTime}',
                         int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.9),
                         TEXT_COLOR)

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

    def on_update(self, delta_time):

        self.max_fps = self.target_fps + TARGET_PLUS_MINUS
        self.min_fps = self.target_fps - TARGET_PLUS_MINUS

        self.shape_list = arcade.ShapeElementList()

        floor = arcade.create_rectangle(
            SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.25),
            SCREEN_WIDTH, SCREEN_HEIGHT // 2,
            FLOOR_COLOR
        )

        ceiling = arcade.create_rectangle(
            SCREEN_WIDTH // 2, int(SCREEN_HEIGHT * 0.75),
            SCREEN_WIDTH, SCREEN_HEIGHT // 2,
            CEILING_COLOR
        )

        self.shape_list.append(floor)
        self.shape_list.append(ceiling)

        # print(f'({self.posX}, {self.posY}) at time {self.time}')

        # arcade.start_render()
        for x in range(0, SCREEN_WIDTH+1, self.render_resolution):
            # calculate the ray position and direction
            cameraX = (2 * x / SCREEN_WIDTH) - 1
            if cameraX > 1 or cameraX < -1:
                print('cameraX is too big or too small!')
                sys.exit()
            #rayDirX = self.dirX + self.planeX * cameraX
            #rayDirY = self.dirY + self.planeY * cameraX
            rayDir = np.empty(2)
            rayDir = self.dir + self.plane * cameraX

            # which box of the map we're in
            #mapX = int(self.posX)
            #mapY = int(self.posY)
            map = np.array([int(self.pos[0]), int(self.pos[1])])

            # print(f'({mapX}, {mapY})')

            # length of ray from current position to the next x- or y-side
            #sideDistX = None
            #sideDistY = None
            sideDist = np.empty(2)

            # length of the ray from one x- or y-side to the next x- or y-side
            deltaDist = np.empty(2)
            try:
                deltaDist[0] = abs(1 / rayDir[0] + 0.0000001)
            except ZeroDivisionError:
                if rayDir[1] == 0:
                    deltaDist[0] = 0
                else:
                    if rayDir[0] == 0:
                        deltaDist[0] = 1
                    else:
                        deltaDist[0] = abs(1 / rayDir[0])
            try:
                deltaDist[1] = abs(1 / rayDir[1] + 0.0000001)
            except ZeroDivisionError:
                if rayDir[0] == 0:
                    deltaDist[1] = 0
                else:
                    if rayDir[1] == 0:
                        deltaDist[1] = 1
                    else:
                        deltaDist[1] = abs(1 / rayDir[1])
            perpWallDist = None

            # which direction to step in the x direction or y direction (either +1 or -1)
            #stepX = None
            #stepY = None
            step = np.empty(2)

            hit = 0  # was there a wall hit?
            side = None  # was a North/South wall hit or an East/West wall hit?
            if rayDir[0] < 0:
                step[0] = -1
                sideDist[0] = (self.pos[0] - map[0]) * deltaDist[0]
            else:
                step[0] = 1
                sideDist[0] = (map[0] + 1.0 - self.pos[0]) * deltaDist[0]

            if rayDir[1] < 0:
                step[1] = -1
                sideDist[1] = (self.pos[1] - map[1]) * deltaDist[1]
            else:
                step[1] = 1
                sideDist[1] = (map[1] + 1.0 - self.pos[1]) * deltaDist[1]

            # was a wall hit? 1 = yes. 0 = no.
            while hit == 0:
                if sideDist[0] < sideDist[1]:
                    sideDist[0] += deltaDist[0]
                    map[0] += step[0]
                    side = 0
                else:
                    sideDist[1] += deltaDist[1]
                    map[1] += step[1]
                    side = 1
                # check if ray has hit a wall
                if self.world_map[map[0]][map[1]] > 0:
                    hit = 1

            if side == 0:
                perpWallDist = (map[0] - self.pos[0] + (1 - step[0]) / 2) / (rayDir[0] + 0.00000001)
            else:
                perpWallDist = (map[1] - self.pos[1] + (1 - step[1]) / 2) / (rayDir[1] + 0.00000001)

            lineHeight = int(SCREEN_HEIGHT / (perpWallDist + 0.00000001))

            drawStart = -lineHeight / 2 + SCREEN_HEIGHT / 2
            if drawStart < 0:
                drawStart = 0

            drawEnd = lineHeight / 2 + SCREEN_HEIGHT / 2
            if drawEnd >= SCREEN_HEIGHT:
                drawEnd = SCREEN_HEIGHT - 1

            if side == 0:
                try:
                    color = self.color_list[self.world_map[map[0]][map[1]]]
                except IndexError:
                    color = arcade.color.YELLOW
            elif side == 1:
                try:
                    color = self.dark_color_list[self.world_map[map[0]][map[1]]]
                except IndexError:
                    color = arcade.color.DARK_YELLOW

            self.shape_list.append(arcade.create_line(x, drawStart, x, drawEnd, color, self.render_resolution))

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

        self.rotation_matrix = np.array([[math.cos(self.rotation_speed), -math.sin(self.rotation_speed)],
                                         [math.sin(self.rotation_speed),  math.cos(self.rotation_speed)]])
        self.rotation_matrix_neg = np.array([[math.cos(-self.rotation_speed), -math.sin(-self.rotation_speed)],
                                             [math.sin(-self.rotation_speed),  math.cos(-self.rotation_speed)]])

        if self.moveForward:
            if not self.world_map[int(self.pos[0] + self.dir[0] * self.move_speed)][int(self.pos[1])]:
                self.pos[0] += self.dir[0] * self.move_speed
            if not self.world_map[int(self.pos[0])][int(self.pos[1] + self.dir[1] * self.move_speed)]:
                self.pos[1] += self.dir[1] * self.move_speed
        elif self.moveBackward:
            if not self.world_map[int(self.pos[0] - self.dir[0] * self.move_speed)][int(self.pos[1])]:
                self.pos[0] -= self.dir[0] * self.move_speed
            if not self.world_map[int(self.pos[0])][int(self.pos[1] - self.dir[1] * self.move_speed)]:
                self.pos[1] -= self.dir[1] * self.move_speed

        if self.strafeLeft:
            if not self.world_map[int(self.pos[0] - self.dir[1] * self.move_speed)][int(self.pos[1])]:
                self.pos[0] -= self.dir[1] * self.move_speed
            if not self.world_map[int(self.pos[0])][int(self.pos[1] + self.dir[0] * self.move_speed)]:
                self.pos[1] += self.dir[0] * self.move_speed
        elif self.strafeRight:
            if not self.world_map[int(self.pos[0] + self.dir[1] * self.move_speed)][int(self.pos[1])]:
                self.pos[0] += self.dir[1] * self.move_speed
            if not self.world_map[int(self.pos[0])][int(self.pos[1] - self.dir[0] * self.move_speed)]:
                self.pos[1] -= self.dir[0] * self.move_speed

        if self.rotateLeft:
            # both camera direction and camera plane must be rotated
            oldDirX = self.dir[0]
            self.dir[0] = self.dir[0] * math.cos(self.rotation_speed) - self.dir[1] * math.sin(self.rotation_speed)
            self.dir[1] = oldDirX * math.sin(self.rotation_speed) + self.dir[1] * math.cos(self.rotation_speed)
            #self.dir*self.rotation_matrix
            oldPlaneX = self.plane[0]
            self.plane[0] = self.plane[0] * math.cos(self.rotation_speed) - self.plane[1] * math.sin(self.rotation_speed)
            self.plane[1] = oldPlaneX * math.sin(self.rotation_speed) + self.plane[1] * math.cos(self.rotation_speed)
            #self.plane*self.rotation_matrix
        elif self.rotateRight:
            # both camera direction and camera plane must be rotated
            oldDirX = self.dir[0]
            self.dir[0] = self.dir[0] * math.cos(-self.rotation_speed) - self.dir[1] * math.sin(-self.rotation_speed)
            self.dir[1] = oldDirX * math.sin(-self.rotation_speed) + self.dir[1] * math.cos(-self.rotation_speed)
            #self.dir*self.rotation_matrix_neg
            oldPlaneX = self.plane[0]
            self.plane[0] = self.plane[0] * math.cos(-self.rotation_speed) - self.plane[1] * math.sin(-self.rotation_speed)
            self.plane[1] = oldPlaneX * math.sin(-self.rotation_speed) + self.plane[1] * math.cos(-self.rotation_speed)
            #self.plane*self.rotation_matrix_neg

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
    game = RaycastingOOP(SCREEN_WIDTH, SCREEN_HEIGHT, "Raycasting in Python")
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
