import sys
import pygame
from pygame.locals import *

pygame.init()

# set up the colors
white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255

# set up the window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame Raycasting")

# draw to the screen surface object
screen.fill(white)
pygame.draw.aaline(screen, blue, (0, 0), (639, 479))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()