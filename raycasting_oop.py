import calculations as calc
import arcade

screenWidth = 640
screenHeight = 480
mapWidth = 7
mapHeight = 7

worldMap = [
    [1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1]
]

posX = 2.5
posY = 3.5

dirX = -1
dirY = 0

planeX = 0
planeY = 0.66

fov = 66

arcade.open_window(screenWidth, screenHeight, "raycasting please work")

arcade.start_render()
for x in range(screenWidth):
    # calculate the ray position and direction
    cameraX = calc.cameraX(x, screenWidth)
    rayDirX = calc.rayDirX(dirX, planeX, cameraX)
    rayDirY = calc.rayDirY(dirY, planeY, cameraX)

    # which box of the map we're in
    mapX = calc.mapX(posX)
    mapY = calc.mapY(posY)

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
    sideDistX = calc.sideDistX(rayDirX, posX, mapX, deltaDistX)
    stepY = calc.stepY(rayDirY)
    sideDistY = calc.sideDistY(rayDirY, posY, mapY, deltaDistY)

    calc.performDDA(hit, sideDistX, sideDistY, mapX, mapY, stepX, stepY, side, deltaDistX, deltaDistY, worldMap)

    perpWallDist = calc.perpWallDist(side, mapX, mapY, posX, posY, stepX, stepY, rayDirX, rayDirY)

    lineHeight = calc.lineHeight(screenHeight, perpWallDist)

    drawStart = calc.drawStart(lineHeight, screenHeight)
    drawEnd = calc.drawEnd(lineHeight, screenHeight)

    arcade.draw_line(x, drawStart, x, drawEnd, arcade.color.BLUE, 3)

arcade.finish_render()
arcade.run()
