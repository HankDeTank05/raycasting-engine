from raycasting_optimized import Vector2


def get_camera_x(pixel_col: int, screen_width: int) -> float:
    """
    returns the x-coordinate in the camera space as a floating-point number
    :param pixel_col:
    the number representing the column of pixels for which the ray will be cast
    :param screen_width:
    the width of the screen, in pixels
    :return:
    """
    return 2 * pixel_col / screen_width - 1


def get_ray_dir_vector(player_direction: Vector2, camera_plane: Vector2, camera_x: float) -> Vector2:
    """
    calculates and returns the direction vector of a ray as a Vector2 object
    :param player_direction:
    :param camera_plane:
    :param camera_x:
    :return:
    """
    ray_dir_x = player_direction.x + camera_plane.x * camera_x
    ray_dir_y = player_direction.y + camera_plane.y * camera_x
    return Vector2(ray_dir_x, ray_dir_y)
