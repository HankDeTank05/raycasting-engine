import math
import sys

import calculations as calc
import arcade

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 160

TEX_WIDTH = 64
TEX_HEIGHT = 64

RENDER_RESOLUTION = 50
TARGET_FPS = 15
TARGET_PLUSMINUS = 2
mapScale = 1


class RaycastingOOP(arcade.Window):
    """
    Main applicaiton class
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.minFPS = None
        self.renderResolution = RENDER_RESOLUTION
        self.maxFPS = None
        self.targetFPS = None
        self.mapWidth = None
        self.mapHeight = None

        self.worldMap = None

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

        self.moveSpeed = None
        self.rotationSpeed = None

        self.shape_list = None

    def setup(self):
        self.mapWidth = 24
        self.mapHeight = 24

        self.worldMap = [
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

        self.posX = 22
        self.posY = 12

        self.dirX = -1.0
        self.dirY = 0.0

        self.planeX = 0
        self.planeY = 0.66

        self.drawStart = []
        self.drawEnd = []

        self.moveForward = False
        self.moveBackward = False
        self.strafeLeft = False
        self.strafeRight = False
        self.rotateLeft = False
        self.rotateRight = False

        self.time = 0

        self.targetFPS = TARGET_FPS

        self.shape_list = arcade.ShapeElementList()

    def on_draw(self):
        arcade.start_render()

        self.shape_list.draw()

        arcade.draw_text(f"Target FPS:\n- <== {self.targetFPS} ==> +",
                         int(SCREEN_WIDTH * 0.1), int(SCREEN_HEIGHT * 0.1),
                         arcade.color.ORANGE)

        arcade.draw_text(f'FPS: {1.0 / self.frameTime}',
                         SCREEN_WIDTH // 2 - 30, int(SCREEN_HEIGHT * 0.9),
                         arcade.color.SAPPHIRE_BLUE)

        arcade.draw_lrtb_rectangle_filled(0 * mapScale, 24 * mapScale, 24 * mapScale, 0 * mapScale,
                                          arcade.color.BLACK)

        arcade.draw_lrtb_rectangle_outline(0 * mapScale, 24 * mapScale, 24 * mapScale, 0 * mapScale,
                                           arcade.color.RED,
                                           mapScale)

        # draw the player location indicator
        arcade.draw_point((self.posX) * mapScale, (24 - self.posY) * mapScale,
                          arcade.color.ORANGE,
                          mapScale)

        # arcade.draw_line(8*mapScale,1*mapScale,1*mapScale,1*mapScale,arcade.color.WHITE,mapScale)
        # arcade.draw_line(1*mapScale,1*mapScale,1*mapScale,7*mapScale,arcade.color.WHITE,mapScale)
        arcade.draw_line_strip(
            [[8 * mapScale, 1 * mapScale],
             [1 * mapScale, 1 * mapScale],
             [1 * mapScale, 7 * mapScale],
             [3 * mapScale, 7 * mapScale],
             [3 * mapScale, 6 * mapScale],
             [3 * mapScale, 7 * mapScale],
             [8 * mapScale, 7 * mapScale],
             [8 * mapScale, 3 * mapScale],
             [3 * mapScale, 3 * mapScale],
             [3 * mapScale, 4 * mapScale]],
            arcade.color.WHITE, mapScale)
        arcade.draw_line_strip(
            [[6 * mapScale, 20 * mapScale],
             [11 * mapScale, 20 * mapScale],
             [11 * mapScale, 15 * mapScale],
             [6 * mapScale, 15 * mapScale],
             [6 * mapScale, 20 * mapScale]],
            arcade.color.GREEN,
            mapScale
        )
        arcade.draw_points(
            [[16 * mapScale, 20 * mapScale],
             [18 * mapScale, 20 * mapScale],
             [20 * mapScale, 20 * mapScale],
             [20 * mapScale, 18 * mapScale],
             [20 * mapScale, 16 * mapScale],
             [18 * mapScale, 16 * mapScale],
             [16 * mapScale, 16 * mapScale],
             [16 * mapScale, 18 * mapScale]],
            arcade.color.BLUE,
            mapScale
        )

        arcade.draw_point(6 * mapScale, 5 * mapScale,
                          arcade.color.YELLOW,
                          mapScale)

    def on_update(self, delta_time):

        self.maxFPS = self.targetFPS + TARGET_PLUSMINUS
        self.minFPS = self.targetFPS - TARGET_PLUSMINUS

        self.shape_list = arcade.ShapeElementList()

        # print(f'({self.posX}, {self.posY}) at time {self.time}')

        # arcade.start_render()
        for x in range(0, SCREEN_WIDTH, self.renderResolution):
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
                if self.worldMap[mapX][mapY] > 0:
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

            if side == 0:
                if self.worldMap[mapX][mapY] == 1:
                    color = arcade.color.RED
                elif self.worldMap[mapX][mapY] == 2:
                    color = arcade.color.GREEN
                elif self.worldMap[mapX][mapY] == 3:
                    color = arcade.color.BLUE
                elif self.worldMap[mapX][mapY] == 4:
                    color = arcade.color.WHITE
                else:
                    color = arcade.color.YELLOW
            elif side == 1:
                if self.worldMap[mapX][mapY] == 1:
                    color = arcade.color.DARK_RED
                elif self.worldMap[mapX][mapY] == 2:
                    color = arcade.color.DARK_GREEN
                elif self.worldMap[mapX][mapY] == 3:
                    color = arcade.color.DARK_BLUE
                elif self.worldMap[mapX][mapY] == 4:
                    color = arcade.color.GRAY
                else:
                    color = arcade.color.DARK_YELLOW

            self.shape_list.append(arcade.create_line(x, drawStart, x, drawEnd, color, self.renderResolution))

        self.oldTime = self.time
        self.time += delta_time

        self.frameTime = (self.time - self.oldTime)  # frameTime is the time this frame has taken in seconds
        # print(1.0 / self.frameTime)  # FPS counter
        FPS = 1 / self.frameTime
        if FPS < self.minFPS:
            self.renderResolution += 1
        elif FPS > self.maxFPS:
            self.renderResolution -= 1
        self.moveSpeed = self.frameTime * 5.0  # constant value in squares/second
        self.rotationSpeed = self.frameTime * 1.5  # constant value in radians/second

        if self.moveForward:
            if not self.worldMap[int(self.posX + self.dirX * self.moveSpeed)][int(self.posY)]:
                self.posX += self.dirX * self.moveSpeed
            if not self.worldMap[int(self.posX)][int(self.posY + self.dirY * self.moveSpeed)]:
                self.posY += self.dirY * self.moveSpeed
        elif self.moveBackward:
            if not self.worldMap[int(self.posX - self.dirX * self.moveSpeed)][int(self.posY)]:
                self.posX -= self.dirX * self.moveSpeed
            if not self.worldMap[int(self.posX)][int(self.posY - self.dirY * self.moveSpeed)]:
                self.posY -= self.dirY * self.moveSpeed

        if self.strafeLeft:
            if not self.worldMap[int(self.posX - self.dirY * self.moveSpeed)][int(self.posY)]:
                self.posX -= self.dirY * self.moveSpeed
            if not self.worldMap[int(self.posX)][int(self.posY + self.dirX * self.moveSpeed)]:
                self.posY += self.dirX * self.moveSpeed
        elif self.strafeRight:
            if not self.worldMap[int(self.posX + self.dirY * self.moveSpeed)][int(self.posY)]:
                self.posX += self.dirY * self.moveSpeed
            if not self.worldMap[int(self.posX)][int(self.posY - self.dirX * self.moveSpeed)]:
                self.posY -= self.dirX * self.moveSpeed

        if self.rotateLeft:
            # both camera direction and camera plane must be rotated
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(self.rotationSpeed) - self.dirY * math.sin(self.rotationSpeed)
            self.dirY = oldDirX * math.sin(self.rotationSpeed) + self.dirY * math.cos(self.rotationSpeed)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(self.rotationSpeed) - self.planeY * math.sin(self.rotationSpeed)
            self.planeY = oldPlaneX * math.sin(self.rotationSpeed) + self.planeY * math.cos(self.rotationSpeed)
        elif self.rotateRight:
            # both camera direction and camera plane must be rotated
            oldDirX = self.dirX
            self.dirX = self.dirX * math.cos(-self.rotationSpeed) - self.dirY * math.sin(-self.rotationSpeed)
            self.dirY = oldDirX * math.sin(-self.rotationSpeed) + self.dirY * math.cos(-self.rotationSpeed)
            oldPlaneX = self.planeX
            self.planeX = self.planeX * math.cos(-self.rotationSpeed) - self.planeY * math.sin(-self.rotationSpeed)
            self.planeY = oldPlaneX * math.sin(-self.rotationSpeed) + self.planeY * math.cos(-self.rotationSpeed)

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
            self.targetFPS -= 1
        if key == arcade.key.E:
            self.targetFPS += 1

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


def main():
    game = RaycastingOOP(SCREEN_WIDTH, SCREEN_HEIGHT, "raycasting work please")
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
