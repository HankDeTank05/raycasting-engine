import math

import calculations as calc
import arcade

screenWidth = 640
screenHeight = 480
renderResolution = 4
mapScale = 5


class RaycastingOOP(arcade.Window):
    """
    Main applicaiton class
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
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
        self.rotateLeft = None
        self.rotateRight = None

        self.time = None
        self.oldTime = None

        self.frameTime = None

        self.moveSpeed = None
        self.rotationSpeed = None

    def setup(self):
        self.mapWidth = 24
        self.mapHeight = 24

        self.worldMap = [
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
        self.rotateLeft = False
        self.rotateRight = False

        self.time = 0

    def on_draw(self):
        pass

    def on_update(self, delta_time):

        print(f'({self.posX}, {self.posY}) at time {self.time}')

        self.drawStart = []
        self.drawEnd = []

        arcade.start_render()
        for x in range(0, screenWidth, renderResolution):
            # calculate the ray position and direction
            cameraX = calc.cameraX(x, screenWidth)
            rayDirX = calc.rayDirX(self.dirX, self.planeX, cameraX)
            rayDirY = calc.rayDirY(self.dirY, self.planeY, cameraX)

            # which box of the map we're in
            mapX = int(self.posX)
            mapY = int(self.posY)

            # length of ray from current position to the next x- or y-side
            sideDistX = None
            sideDistY = None

            # length of the ray from one x- or y-side to the next x- or y-side
            deltaDistX = calc.deltaDistX_forRatio(rayDirX, rayDirY)
            deltaDistY = calc.deltaDistY_forRatio(rayDirY, rayDirY)
            perpWallDist = None

            # which directon to step in the x direction or y direction (either +1 or -1)
            stepX = None
            stepY = None

            hit = 0  # was there a wall hit?
            side = None  # was a North/South wall hit or an East/West wall hit?
            stepX = calc.stepX(rayDirX)
            sideDistX = calc.sideDistX(rayDirX, self.posX, mapX, deltaDistX)
            stepY = calc.stepY(rayDirY)
            sideDistY = calc.sideDistY(rayDirY, self.posY, mapY, deltaDistY)

            # was a wall hit? 1 = yes. 0 = no.
            while hit == 0:
                if sideDistX > sideDistY:
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

            lineHeight = int(screenHeight / (perpWallDist + 0.00000001))

            drawStart = -lineHeight / 2 + screenHeight / 2
            if drawStart < 0:
                drawStart = 0

            drawEnd = lineHeight / 2 + screenHeight / 2
            if drawEnd >= screenHeight:
                drawEnd = screenHeight - 1

            if self.worldMap[mapX][mapY] == 1:
                arcade.draw_line(x, drawStart, x, drawEnd, arcade.color.RED, renderResolution)
            elif self.worldMap[mapX][mapY] == 2:
                arcade.draw_line(x, drawStart, x, drawEnd, arcade.color.GREEN, renderResolution)
            elif self.worldMap[mapX][mapY] == 3:
                arcade.draw_line(x, drawStart, x, drawEnd, arcade.color.BLUE, renderResolution)
            elif self.worldMap[mapX][mapY] == 4:
                arcade.draw_line(x, drawStart, x, drawEnd, arcade.color.WHITE, renderResolution)
            else:
                arcade.draw_line(x, drawStart, x, drawEnd, arcade.color.YELLOW, renderResolution)

            '''self.drawStart.append(drawStart)
            self.drawEnd.append(drawEnd)'''

        self.oldTime = self.time
        self.time += delta_time

        self.frameTime = (self.time - self.oldTime) / 10  # frameTime is the time this frame has taken in seconds
        print(1.0 / self.frameTime)  # FPS counter

        self.moveSpeed = self.frameTime * 5.0  # constant value in squares/second
        self.rotationSpeed = self.frameTime * 3.0  # constant value in radians/second

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

        arcade.draw_lrtb_rectangle_outline(0 * mapScale, 24 * mapScale, 24 * mapScale, 0 * mapScale,
                                           arcade.color.RED,
                                           mapScale)

        # draw the player location indicator
        arcade.draw_point((self.posY) * mapScale, (24-self.posX) * mapScale,
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            print('W/UP')
            self.moveForward = True
        if key == arcade.key.A:
            print('A/LEFT')
            self.rotateLeft = True
        if key == arcade.key.S:
            print('S/DOWN')
            self.moveBackward = True
        if key == arcade.key.D:
            print('D/RIGHT')
            self.rotateRight = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.moveForward = False
        if key == arcade.key.S:
            self.moveBackward = False
        if key == arcade.key.A:
            self.rotateLeft = False
        if key == arcade.key.D:
            self.rotateRight = False


def main():
    game = RaycastingOOP(screenWidth, screenHeight, "raycasting work please")
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
