import math

import pygame
import sys
import numpy as np
import pygame_version.helpers as helper

pygame.init()

screen_size = screen_width, screen_height = 640, 480

world_map = np.array(
    [
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
)

black = 0, 0, 0
red = 255, 0, 0
green = 0, 255, 0
blue = 0, 0, 255
white = 255, 255, 255

screen = pygame.display.set_mode(screen_size)

pos_x, pos_y = 22, 12  # player starting position
dir_x, dir_y = -1, 0  # direction they are facing to start (direction vector)
plane_x, plane_y = 0, 0.66  # camera plane (perpendicular to direction vector)

time = 0  # time of the current frame
old_time = 0  # time of the previous frame

clock = pygame.time.Clock()

constant_move_speed = 5.0
constant_rotation_speed = 3.0

move_forward = False
move_backward = False
rotate_left = False
rotate_right = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # process the game logic
    for pixel_col in range(screen_width):
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

        print(f'{side_dist_x}, {side_dist_y}')
        # DDA
        side = helper.perform_dda_algorithm(map_x, map_y, step_x, step_y,
                                            side_dist_x, side_dist_y, delta_dist_x, delta_dist_y,
                                            world_map)

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

        # determine the wall color
        if world_map[map_x, map_y] == 1:
            color = [255, 0, 0]  # red
        elif world_map[map_x, map_y] == 2:
            color = [0, 255, 0]  # green
        elif world_map[map_x, map_y] == 3:
            color = [0, 0, 255]  # blue
        elif world_map[map_x, map_y] == 4:
            color = [255, 255, 255]  # white
        else:
            color = [255, 255, 0]  # yellow

        if side == 1:
            for val in range(len(color)):
                color[val] /= 2

        color = tuple(color)

        # draw the column of pixels
        pygame.draw.line(screen, color, (pixel_col, int(draw_start)), (pixel_col, int(draw_end)), width=1)

    old_time = time  # the time (in milliseconds) of the last frame
    time = clock.get_time()  # the time (in milliseconds) of the current frame

    # the amount of time this frame has spent onscreen (in seconds)
    frame_time = (time - old_time) / 1000

    # update the screen
    pygame.display.fill(black)
    pygame.display.flip()

    clock.tick()

    move_speed = frame_time * constant_move_speed
    rotation_speed = frame_time * constant_rotation_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            for key in pygame.key.get_pressed():
                if key == pygame.K_LEFT:
                    # rotate to the left (camera direction and camera plane must be rotated)
                    old_dir_x = dir_x
                    dir_x = dir_x * math.cos(rotation_speed) - dir_y * math.sin(rotation_speed)
                    dir_y = old_dir_x * math.sin(rotation_speed) + dir_y * math.cos(rotation_speed)
                    old_plane_x = plane_x
                    plane_x = plane_x * math.cos(rotation_speed) - plane_y * math.sin(rotation_speed)
                    plane_y = old_plane_x * math.sin(rotation_speed) + plane_y * math.cos(rotation_speed)
                    # rotate_left = True

                if key == pygame.K_RIGHT:
                    # rotate to the right (camera direction and camera plane must be rotated)
                    old_dir_x = dir_x
                    dir_x = dir_x * math.cos(-rotation_speed) - dir_y * math.sin(-rotation_speed)
                    dir_y = old_dir_x * math.sin(-rotation_speed) + dir_y * math.cos(-rotation_speed)
                    old_plane_x = plane_x
                    plane_x = plane_x * math.cos(-rotation_speed) - plane_y * math.sin(-rotation_speed)
                    plane_y = old_plane_x * math.sin(-rotation_speed) + plane_y * math.cos(-rotation_speed)
                    # rotate_right = True

                if key == pygame.K_UP:
                    # move forward if there's no wall in front of you
                    if not world_map[int(pos_x + dir_x * move_speed), int(pos_y)]:
                        pos_x += dir_x * move_speed
                    if not world_map[int(pos_x), int(pos_y + dir_y * move_speed)]:
                        pos_y += dir_y * move_speed
                    # move_forward = True

                if key == pygame.K_DOWN:
                    # move backward if there's no wall behind you
                    if not world_map[int(pos_x - dir_x * move_speed), int(pos_y)]:
                        pos_x -= dir_x * move_speed
                    if not world_map[int(pos_x), int(pos_y - dir_y * move_speed)]:
                        pos_y -= dir_y * move_speed
                    # move_backward = True
        # elif event.type == pygame.KEYUP:
        #     for key in pygame.key.get_pressed():
        #         if key == pygame.K_LEFT:
        #             rotate_left = False
        #         if key == pygame.K_RIGHT:
        #             rotate_right = False
        #         if key == pygame.K_UP:
        #             move_forward = False
        #         if key == pygame.K_DOWN:
        #             move_forward = False
