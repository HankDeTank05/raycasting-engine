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

if __name__ == "__main__":
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
    print('TESTING fov(dirX, dirY, planeX, planeY)')
    print(f'this should be 66: {fov(-1, 0, 0, 0.66)}')
    print(f'this should be 66: {fov(dirX, dirY, planeX, planeY)}')
    print()
    print('TESTING cameraX(columnX, screenWidth)')
    print(f'this should be -1: {cameraX(0, 100)}')
    print(f'this should be 0: {cameraX(50, 100)}')
    print(f'this hsould be 1: {cameraX(100, 100)}')
    print()
