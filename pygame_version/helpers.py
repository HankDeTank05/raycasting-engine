import pygame
import os


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


def get_camera_x(pixel_col: int, screen_width: int):
    """
    get the x-coordinate in camera space
    :param pixel_col:
    :param screen_width:
    :return:
    """
    return 2 * pixel_col / screen_width - 1


def get_ray_dir_xy(dir_xy, plane_xy, camera_x):
    """
    get the x-component or the y-component of a ray's direction vector.

    NOTE: you MUST pass the same axis variables for both dir_xy and plane_xy. For example, if you pass dir_x for the
    dir_xy parameter, you MUST pass plane_x for the plane_xy parameter, and vice-versa.
    :param dir_xy:
    :param plane_xy:
    :param camera_x:
    :return:
    """
    return dir_xy + plane_xy * camera_x


def get_ray_dirs(dir_x, dir_y, plane_x, plane_y, camera_x):
    """
    get the x- and y-components of a ray's direction vector
    :param dir_x:
    :param dir_y:
    :param plane_x:
    :param plane_y:
    :param camera_x:
    :return:
    """
    return get_ray_dir_xy(dir_x, plane_x, camera_x), get_ray_dir_xy(dir_y, plane_y, camera_x)


def get_delta_dist_x(ray_dir_x, ray_dir_y):
    """
    calculate the distance between any two adjacent VERTICAL grid-lines.

    NOTE: this is NOT THE SAME AS get_delta_dist_y!!!
    :param ray_dir_x:
    :param ray_dir_y:
    :return:
    """
    if ray_dir_y == 0:
        return 0
    elif ray_dir_x == 0:
        return 1
    else:
        return abs(1 / ray_dir_x)


def get_delta_dist_y(ray_dir_x, ray_dir_y):
    """
    calculate the distance between any two adjacent HORIZONTAL grid-lines

    NOTE: this is NOT THE SAME AS get_delta_dist_x!!!
    :param ray_dir_x:
    :param ray_dir_y:
    :return:
    """
    if ray_dir_x == 0:
        return 0
    elif ray_dir_y == 0:
        return 1
    else:
        return abs(1 / ray_dir_y)


def get_step_and_side_dist_xy(ray_dir_xy, pos_xy, map_xy, delta_dist_xy):
    """
    calculate the step values and the side_dist values.

    NOTE: you MUST pass the same axis variables for all param_xy parameters!!! For example, if you pass ray_dir_x for
    the parameter ray_dir_xy, you MUST pass pos_x for the pos_xy parameter, map_x for map_xy, etc., and vice-versa for
    the y-axis variables

    :param ray_dir_xy:
    :param pos_xy:
    :param map_xy:
    :param delta_dist_xy:
    :return: step_xy, side_dist_xy
    """
    if ray_dir_xy < 0:
        return -1, (pos_xy - map_xy) * delta_dist_xy  # return step_xy, side_dist_xy
    else:
        return 1, (map_xy + 1 - pos_xy) * delta_dist_xy  # return step_xy, side_dist_xy


def perform_dda_algorithm(map_x, map_y, step_x, step_y, side_dist_x, side_dist_y, delta_dist_x, delta_dist_y,
                          world_map):
    while True:
        if side_dist_x < side_dist_y:
            side_dist_x += delta_dist_x
            map_x += step_x
            side = 0
        else:
            side_dist_y += delta_dist_y
            map_y += step_y
            side = 1
        if world_map[map_x, map_y] > 0:
            return side


def get_perp_wall_dist(map_xy, pos_xy, step_xy, ray_dir_xy):
    return (map_xy - pos_xy + (1 - step_xy) / 2) / ray_dir_xy
