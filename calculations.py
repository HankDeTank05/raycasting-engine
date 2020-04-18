import math

posX = None
posY = None

dirX = -1
dirY = 0

planeX = 0
planeY = 0.66

def fov(dirX, dirY, planeX, planeY):
    dirLength = vectorLength(dirX, dirY)
    planeLength = vectorLength(planeX, planeY)
    fov = 2 * math.atan( planeLength/dirLength )
    return math.degrees(fov)

def vectorLength(vx, vy):
    return math.sqrt(vx**2 + vy**2)

def cameraX(columnX, screenWidth):
    return (2 * columnX / screenWidth) - 1

def rayDirX(dirX, planeX, cameraX):
    # logically and functionally equivalent to rayDirY()
    return dirX + planeX * cameraX

def rayDirY(dirY, planeY, cameraX):
    # logically and functionally equivalent to rayDirX()
    return dirY + planeY * cameraX

def mapX(posX):
    # logically and functionally equivalent to mapY()
    return int(posX)

def mapY(posY):
    # logically and functionally equivalent to mapX()
    return int(posY)

def sideDistX(rayDirX, posX, mapX, deltaDistX):
    if rayDirX < 0:
        return (posX - mapX) * deltaDistX
    else:
        return (mapX + 1.0 - posX) * deltaDistX

def sideDistY(rayDirY, posY, mapY, deltaDistY):
    if rayDirY < 0:
        return (posY - mapY) * deltaDistY
    else:
        return (mapY + 1.0 - posY) * deltaDistY

def deltaDistX_pythagorean(rayDirX, rayDirY):
    # NOT EQUIVALENT TO deltaDistY_pythagorean()
    return math.sqrt(1 + (rayDirY**2) / (rayDirX**2))

def deltaDistY_pythagorean(rayDirX, rayDirY):
    # NOT EQUIVALENT TO deltaDistX_pythagorean()
    return math.sqrt(1 + (rayDirX**2) / (rayDirY**2))

def v(rayDirX, rayDirY):
    return math.sqrt(rayDirX**2 + rayDirY**2)

def deltaDistX_simplified(rayDirX, rayDirY):
    return abs(abs(v(rayDirX, rayDirY)) / rayDirX)

def deltaDistY_simplified(rayDirX, rayDirY):
    return abs(abs(v(rayDirX, rayDirY)) / rayDirY)

def deltaDistX_forRatio(rayDirX, rayDirY):
    # NOT EQUIVALENT TO deltaDistY_forRatio
    try:
        return abs(1/rayDirX)
    except ZeroDivisionError:
        if rayDirY == 0:
            return 0
        else:
            if rayDirX == 0:
                return 1
            else:
                return abs(1 / rayDirX)

def deltaDistY_forRatio(rayDirX, rayDirY):
    # NOT EQUIVALENT TO deltaDistX_forRatio
    try:
        return abs(1/rayDirY)
    except ZeroDivisionError:
        if rayDirX == 0:
            return 0
        else:
            if rayDirY == 0:
                return 1
            else:
                return abs(1 / rayDirY)

def perpWallDist(side, mapX, mapY, posX, posY, stepX, stepY, rayDirX, rayDirY):
    if side == 0:
        return (mapX - posX + (1 - stepX) / 2) / (rayDirX + 0.00000001)
    else:
        return (mapY - posY + (1 - stepY) / 2) / (rayDirY + 0.00000001)

def stepX(rayDirX):
    # logically and functonally equivalent to stepY()
    if rayDirX < 0:
        return -1
    else:
        return 1

def stepY(rayDirY):
    # logically and functonally equivalent to stepX()
    if rayDirY < 0:
        return -1
    else:
        return 1

def performDDA(hit, sideDistX, sideDistY, mapX, mapY, stepX, stepY, side, deltaDistX, deltaDistY, worldMap):
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
        if worldMap[mapX][mapY] > 0:
            hit = 1

def lineHeight(screenHeight, perpWallDist):
    return int(screenHeight / perpWallDist)

def drawStart(lineHeight, screenHeight):
    drawStart = -lineHeight / 2 + screenHeight / 2
    if drawStart < 0:
        return 0
    else:
        return drawStart

def drawEnd(lineHeight, screenHeight):
    drawEnd = lineHeight / 2 + screenHeight / 2
    if drawEnd >= screenHeight:
        return screenHeight - 1
    else:
        return drawEnd

if __name__ == "__main__":
    # test vectorLength()
    print('TESTING vectorLength(vx, vy)')
    print(f'this should be 5.0: {vectorLength(3,4)}')
    print(f'this should be 13.0: {vectorLength(5,12)}')
    print('these next two should be the same')
    print(vectorLength(10,10))
    print(10*math.sqrt(2))
    print()
    print('TESTING math.degrees(2 * math.atan( 0.66/1 ))')
    print(f'this should be 66: {math.degrees(2 * math.atan( 0.66/1 ))}')
    print('TESTING 2 * math.degrees(math.atan( 0.66/1 ))')
    print(f'this should be 66: {2 * math.degrees(math.atan( 0.66/1 ))}')
    print()
    # test fov()
    print('TESTING fov(dirX, dirY, planeX, planeY)')
    print(f'this should be 66: {fov(-1, 0, 0, 0.66)}')
    print(f'this should be 66: {fov(dirX, dirY, planeX, planeY)}')
    print()
    # test cameraX()
    cX = []
    cX.append(cameraX(0,100))
    cX.append(cameraX(50,100))
    cX.append(cameraX(100,100))
    print('TESTING cameraX(columnX, screenWidth)')
    print(f'this should be -1: {cameraX(0, 100)}')
    print(f'this should be 0: {cameraX(50, 100)}')
    print(f'this hsould be 1: {cameraX(100, 100)}')
    print()
    # test rayDirX()
    print('TESTING rayDirX(dirX, planeX, cameraX)')
    print('all of the following should be -1')
    for column in cX:
        print(rayDirX(dirX, planeX, column))
        print(rayDirY(dirX, planeX, column))
    # test rayDirY()
    for column in cX:
        print(rayDirY(dirY, planeY, column))
        print(rayDirX(dirY, planeY, column))
    # test deltaDistX_pythagorean()
    # test deltaDistY_pythagorean()
    # test v()
    # test deltaDistX_simplified()
    # test deltaDistY_simplified()
    # test deltaDistX_forRatio()
    # test deltaDistY_forRatio()
    # test stepX()
    # test stepY()
