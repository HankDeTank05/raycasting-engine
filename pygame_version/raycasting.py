import math
import pygame
import sys
import numpy as np
import helpers as helper
import time
import copy
import os
# from OpenGL.GL import *
# from OpenGL.GLU import *


def load_image(name, colorkey=None):
    fullname = os.path.join('pics', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image


pygame.init()

screen_size = screen_width, screen_height = 128, 100

player_height = screen_height / 2

world_map = np.array([
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

black = 0, 0, 0
red = 255, 0, 0
yellow = 255, 255, 0
green = 0, 255, 0
cyan = 0, 255, 255
blue = 0, 0, 255
purple = 255, 0, 255
white = 255, 255, 255

screen = pygame.display.set_mode(screen_size, flags=pygame.SCALED)
pygame.display.set_caption("Pygame Raycasting")

# void gluPerspective(GLdouble fovy, GLdouble aspect, GLdouble zNear, GLdouble zFar);
# gluPerspective(60, (screen_size[0]/screen_size[1]), 0.1, 100.0)

pos_x, pos_y = 22, 12  # player starting position
dir_x, dir_y = -1, 0  # direction they are facing to start (direction vector)
plane_x, plane_y = 0, 0.66  # camera plane (perpendicular to direction vector)

current_time = 0  # time of the current frame
old_time = 0  # time of the previous frame

clock = pygame.time.Clock()

constant_move_speed = 5.0
constant_rotation_speed = -3.0

move_forward = False
move_backward = False
rotate_left = False
rotate_right = False

draw_points = []
draw_colors = []

lod = 1

pixels = pygame.PixelArray(screen)

tex_height = 64
tex_width = 64

texture = []

for tex in range(8):
    texture.append([])
    if tex == 0:
        texture[tex] = load_image('eagle.png')
    if tex == 1:
        texture[tex] = load_image('redbrick.png')
    if tex == 2:
        texture[tex] = load_image('purplestone.png')
    if tex == 3:
        texture[tex] = load_image('greystone.png')
    if tex == 4:
        texture[tex] = load_image('bluestone.png')
    if tex == 5:
        texture[tex] = load_image('mossy.png')
    if tex == 6:
        texture[tex] = load_image('wood.png')
    if tex == 7:
        texture[tex] = load_image('colorstone.png')
    # texture[tex] = tuple(texture[tex])

# for i in range(8):
#     for x in range(tex_width):
#         for y in range(x):
#             texture[i][tex_width * y + x], texture[i][tex_width * x + y] = texture[i][tex_width * y + x], texture[i][tex_width * x + y]
#     texture[i] = tuple(texture[i])

texture = tuple(texture)

floor_texture = 3
ceiling_texture = 6

floorcast_tech = ['scanline', 'vertical']
floorcast_method = 'vertical'

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rotate_left = True
            if event.key == pygame.K_RIGHT:
                rotate_right = True
            if event.key == pygame.K_UP:
                move_forward = True
            if event.key == pygame.K_DOWN:
                move_backward = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                rotate_left = False
            if event.key == pygame.K_RIGHT:
                rotate_right = False
            if event.key == pygame.K_UP:
                move_forward = False
            if event.key == pygame.K_DOWN:
                move_backward = False

    # print(f'pos_x, pos_y = {pos_x}, {pos_y}')

    if move_forward:
        # move forward if there's no wall in front of you
        if not world_map[int(pos_x + dir_x * move_speed), int(pos_y)]:
            pos_x += dir_x * move_speed
        if not world_map[int(pos_x), int(pos_y + dir_y * move_speed)]:
            pos_y += dir_y * move_speed
        pass
    elif move_backward:
        # move backward if there's no wall behind you
        if not world_map[int(pos_x - dir_x * move_speed), int(pos_y)]:
            pos_x -= dir_x * move_speed
        if not world_map[int(pos_x), int(pos_y - dir_y * move_speed)]:
            pos_y -= dir_y * move_speed

    if rotate_left:
        # rotate to the right (camera direction and camera plane must be rotated)
        old_dir_x = dir_x
        dir_x = dir_x * math.cos(-rotation_speed) - dir_y * math.sin(-rotation_speed)
        dir_y = old_dir_x * math.sin(-rotation_speed) + dir_y * math.cos(-rotation_speed)
        old_plane_x = plane_x
        plane_x = plane_x * math.cos(-rotation_speed) - plane_y * math.sin(-rotation_speed)
        plane_y = old_plane_x * math.sin(-rotation_speed) + plane_y * math.cos(-rotation_speed)
        pass
    elif rotate_right:
        # rotate to the left (camera direction and camera plane must be rotated)
        old_dir_x = dir_x
        dir_x = dir_x * math.cos(rotation_speed) - dir_y * math.sin(rotation_speed)
        dir_y = old_dir_x * math.sin(rotation_speed) + dir_y * math.cos(rotation_speed)
        old_plane_x = plane_x
        plane_x = plane_x * math.cos(rotation_speed) - plane_y * math.sin(rotation_speed)
        plane_y = old_plane_x * math.sin(rotation_speed) + plane_y * math.cos(rotation_speed)
        pass

    # process the game logic
    screen.fill(black)

    if floorcast_method == floorcast_tech[0]:
        # *************
        # FLOOR CASTING method 1: scanline
        # this method renders in horizontal scanlines, and renders the whole screen's pixels. This is inefficient
        # because some pixels are drawn over again when casting for walls
        # *************
        for pixel_row in range(0, screen_height, lod):

            # ray direction for the leftmost ray (x = 0)
            ray_dir_x0 = dir_x - plane_x
            ray_dir_y0 = dir_y - plane_y

            # ray direction for the rightmost ray (x = screen_width)
            ray_dir_x1 = dir_x + plane_x
            ray_dir_y1 = dir_y + plane_y

            # current y position compared to the center of the screem
            p = int(pixel_row - screen_height / 2)

            if p == 0:
                continue

            # vertical position of the camera
            pos_z = float(0.5 * screen_height)

            # horizontal distance from the camera to the floor for the current row
            # 0.5 is the current z position exactly in the middle between the floor and the ceiling
            row_distance = float(pos_z / p)

            # calculate the real-world step vector we have to add for each x (parallel to the camera plane)
            # adding step-by-step avoids multiplication with a weight in the inner loop
            floor_step_x = row_distance * (ray_dir_x1 - ray_dir_x0) / screen_width
            floor_step_y = row_distance * (ray_dir_y1 - ray_dir_y0) / screen_width

            # real-world coordinates of the leftmost column. this will be updated as we step to the right
            floor_x = pos_x + row_distance * ray_dir_x0
            floor_y = pos_y + row_distance * ray_dir_y0

            for pixel_col in range(0, screen_width, lod):
                # the cell coordinate is simply gotten from truncating floor_x and floor_y
                cell_x = int(floor_x)
                cell_y = int(floor_y)

                # get the texture coordinate from the fractional part that was truncated off
                tx = int(tex_width * (floor_x - cell_x))
                if tx < 0:
                    tx = 0
                elif tx >= tex_width:
                    tx = tex_width - 1

                ty = int(tex_height * (floor_y - cell_y))
                if ty < 0:
                    ty = 0
                elif ty >= tex_height:
                    tx = tex_height - 1

                floor_x += floor_step_x
                floor_y += floor_step_y

                # choose a texture and draw the pixel

                # floor
                color = texture[floor_texture].get_at((tx, ty))
                pixels[pixel_col][pixel_row] = color

                # ceiling
                color = texture[ceiling_texture].get_at((tx, ty))
                pixels[pixel_col][screen_height - pixel_row - 1] = color

    # ************
    # WALL CASTING
    # ************
    for pixel_col in range(0, screen_width, lod):
        draw_points = []
        draw_colors = []

        camera_x = helper.get_camera_x(pixel_col, screen_width)
        ray_dir_x, ray_dir_y = helper.get_ray_dirs(dir_x, dir_y, plane_x, plane_y, camera_x)

        # figure out which box of the map we're in
        map_x = int(pos_x)
        map_y = int(pos_y)

        # length of the ray between any vertical grid-line and the next one
        delta_dist_x = helper.get_delta_dist_x(ray_dir_x, ray_dir_y)
        # length of the ray between an horizontal grid-line and the next one
        delta_dist_y = helper.get_delta_dist_y(ray_dir_x, ray_dir_y)

        # calculate step variables and initial side_dist values

        # step_x is the x-direction in which the ray should move when cast (-1 = left, 0 = none, +1 = right)
        # side_dist_x is the length of the ray from its current position to the next vertical grid-line
        step_x, side_dist_x = helper.get_step_and_side_dist_xy(ray_dir_x, pos_x, map_x, delta_dist_x)

        # step_y is the length of the ray from its current position to the next horizontal grid-line
        # side_dist_y is the the y-direction in which the ray should move when cast (-1 = up, 0 = none, +1 = down)
        step_y, side_dist_y = helper.get_step_and_side_dist_xy(ray_dir_y, pos_y, map_y, delta_dist_y)

        # DDA
        hit = 0
        side = None
        distance = 0
        while hit == 0:
            if side_dist_x < side_dist_y:
                side_dist_x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist_y += delta_dist_y
                map_y += step_y
                side = 1
            if world_map[map_x, map_y] > 0:
                hit = 1
            distance += 1

        # calculate the distance to the wall that was hit by the current ray
        if side == 0:
            perp_wall_dist = (map_x - pos_x + (1 - step_x) / 2) / ray_dir_x
        else:
            perp_wall_dist = (map_y - pos_y + (1 - step_y) / 2) / ray_dir_y

        # calculate the height of the pixel column to draw
        line_height = int(screen_height / (perp_wall_dist + 0.0000000001))

        # calculate the lowest and highest pixel to fill in the current column
        draw_start = -line_height / 2 + screen_height / 2
        if draw_start < 0:
            draw_start = 0
        draw_end = line_height / 2 + screen_height / 2
        if draw_end > screen_height:
            draw_end = screen_height - 1

        # # determine the wall color
        # if world_map[map_x][map_y] == 1:
        #     color = [255, 0, 0]  # red
        # elif world_map[map_x][map_y] == 2:
        #     color = [0, 255, 0]  # green
        # elif world_map[map_x][map_y] == 3:
        #     color = [0, 0, 255]  # blue
        # elif world_map[map_x][map_y] == 4:
        #     color = [255, 255, 255]  # white
        # else:
        #     color = [255, 255, 0]  # yellow

        # texturing calculations
        tex_num = world_map[map_x, map_y] - 1  # subtract 1 so that texture[0] can be used

        # calculate the value of wall_x
        wall_x = pos_y + perp_wall_dist * ray_dir_y if side == 0 else pos_x + perp_wall_dist * ray_dir_x
        wall_x -= math.floor(wall_x)

        # x coordinate on the texture
        tex_x = int(wall_x * tex_width)
        if side == 0 and ray_dir_x > 0:
            tex_x = tex_width - tex_x - 1
        if side == 1 and ray_dir_y < 0:
            tex_x = tex_width - tex_x - 1

        # how much to increase the texture coordinate per screen pixel
        step = 1.0 * tex_height / line_height
        # starting texture coordinate
        tex_pos = (draw_start - screen_height / 2 + line_height / 2) * step
        for pixel_row in range(int(draw_start), int(draw_end), lod):
            tex_y = int(tex_pos)
            tex_pos += step
            color = texture[tex_num].get_at((tex_x, tex_y))
            color.a = 255

            if side == 1:
                color.r //= 2
                color.g //= 2
                color.b //= 2

            pixels[pixel_col][pixel_row] = color

        # *************
        # FLOOR CASTING method 2: vertical stripes
        # *************
        if floorcast_method == floorcast_tech[1]:
            # x and y position of the floor texel (texture pixel) at the bottom of the wall
            floor_x_wall, floor_y_wall = None, None

            # 4 different wall directions possible
            if side == 0 and ray_dir_x > 0:
                floor_x_wall = map_x
                floor_y_wall = map_y + wall_x
            elif side == 0 and ray_dir_x < 0:
                floor_x_wall = map_x + 1
                floor_y_wall = map_y + wall_x
            elif side == 1 and ray_dir_y > 0:
                floor_x_wall = map_x + wall_x
                floor_y_wall = map_y
            else:
                floor_x_wall = map_x + wall_x
                floor_y_wall = map_y + 1

            dist_wall, dist_player, current_dist = None, None, None

            dist_wall = perp_wall_dist
            dist_player = 0.0

            if draw_end < 0:
                draw_end = screen_height

            for pixel_row in range(int(draw_end) + 1, screen_height, lod):
                current_dist = screen_height / (2.0 * pixel_row - screen_height)  # you could make a lookup table for this instead

                weight = (current_dist - dist_player) / (dist_wall - dist_player)

                current_floor_x = weight * floor_x_wall + (1.0 - weight) * pos_x
                current_floor_y = weight * floor_y_wall + (1.0 - weight) * pos_y

                floor_tex_x = int(current_floor_x * tex_width) % tex_width
                floor_tex_y = int(current_floor_y * tex_height) % tex_height

                # floor
                pixels[pixel_col][pixel_row] = texture[floor_texture].get_at((floor_tex_x, floor_tex_y))

                # ceiling (symmetrical!)
                pixels[pixel_col][screen_height - pixel_row] = texture[ceiling_texture].get_at((floor_tex_x, floor_tex_y))

            # color = tuple(color)

            # draw_start_pair = (pixel_col, int(draw_start))
            # draw_end_pair = (pixel_col, int(draw_end))
            # print(draw_start_pair)
            # print(draw_end_pair)
            # print()

            # store the points and colors for drawing later
            # draw_points.append((draw_start_pair, draw_end_pair))
            # draw_colors.append(color)
            # pygame.draw.line(screen, color, draw_start_pair, draw_end_pair, lod)
            # for pixel_row in range(int(draw_start), int(draw_end), lod):
            #     pixels[pixel_col][pixel_row] = color

    old_time = current_time  # the time (in milliseconds) of the last frame
    current_time = time.time()  # the time (in milliseconds) of the current frame

    # the amount of time this frame has spent onscreen (in seconds)
    frame_time = (current_time - old_time) / 1.0

    FPS = 1 / (frame_time + 0.0000001)
    # print(FPS)

    # if FPS < 25:
    #     lod += 1
    # elif FPS > 35 and lod >= 2:
    #     lod -= 1

    # update the screen
    # screen.fill(black)
    # for col in range(len(draw_points)):
    #     print(draw_points[col][0])
    #     pygame.draw.line(screen, draw_colors[col], draw_points[col][0], draw_points[col][1])
    pygame.display.flip()

    clock.tick(15)

    move_speed = frame_time * constant_move_speed
    rotation_speed = frame_time * constant_rotation_speed
    # print(move_speed)


