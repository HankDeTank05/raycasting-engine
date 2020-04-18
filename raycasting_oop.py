import calculations as calc
import arcade

screenWidth = 200
screenHeight = 150


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

        self.changeX = None
        self.changeY = None
        self.speed = None

        self.time = None
        self.oldTime = None

    def setup(self):
        self.mapWidth = 7
        self.mapHeight = 7

        self.worldMap = [
            [1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1]
        ]

        self.posX = 2.5
        self.posY = 3.5

        self.dirX = 0.5
        self.dirY = 0.5

        self.fov = 66

        self.drawStart = []
        self.drawEnd = []

        self.changeX = 0.0
        self.changeY = 0.0
        self.speed = 0.1

        self.time = 0

    def on_draw(self):
        '''for x in range(len(self.drawStart)):
            pass'''
        pass

    def on_update(self, delta_time):

        self.oldTime = self.time
        self.time += delta_time

        self.posX += self.changeX
        self.posY += self.changeY
        if self.posX >= 5:
            self.posX = 5
        if self.posX <= 1:
            self.posX = 1
        if self.posY >= 5:
            self.posY = 5
        if self.posY <= 1:
            self.posY = 1

        print(f'({self.posX}, {self.posY}) at time {self.time}')
        print(f'{self.changeX}, {self.changeY}')

        self.planeX = -self.dirY
        self.planeY = self.dirX

        self.drawStart = []
        self.drawEnd = []

        arcade.start_render()
        for x in range(screenWidth):
            # calculate the ray position and direction
            cameraX = calc.cameraX(x, screenWidth)
            rayDirX = calc.rayDirX(self.dirX, self.planeX, cameraX)
            rayDirY = calc.rayDirY(self.dirY, self.planeY, cameraX)

            # which box of the map we're in
            mapX = calc.mapX(self.posX)
            mapY = calc.mapY(self.posY)

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

            calc.performDDA(hit, sideDistX, sideDistY, mapX, mapY, stepX, stepY, side, deltaDistX, deltaDistY,
                            self.worldMap)

            perpWallDist = calc.perpWallDist(side, mapX, mapY, self.posX, self.posY, stepX, stepY, rayDirX, rayDirY)

            lineHeight = calc.lineHeight(screenHeight, perpWallDist)

            drawStart = calc.drawStart(lineHeight, screenHeight)
            drawEnd = calc.drawEnd(lineHeight, screenHeight)

            arcade.draw_line(x, drawStart, x, drawEnd, arcade.color.BLUE, 1)

            '''self.drawStart.append(drawStart)
            self.drawEnd.append(drawEnd)'''

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            print('W/UP')
            self.changeY = self.speed
        if key == arcade.key.A:
            print('A/LEFT')
            self.changeX = -self.speed
        if key == arcade.key.S:
            print('S/DOWN')
            self.changeY = -self.speed
        if key == arcade.key.D:
            print('D/RIGHT')
            self.changeX = self.speed

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.S:
            self.changeY = 0
        if key == arcade.key.A or key == arcade.key.D:
            self.changeX = 0


def main():
    game = RaycastingOOP(screenWidth, screenHeight, "raycasting work please")
    game.setup()

    arcade.run()


if __name__ == "__main__":
    main()
