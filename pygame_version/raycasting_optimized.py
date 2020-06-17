import math
import pygame
import sys
import numpy as np
import time
import optimizedhelpers as oh
from typing import List, Union

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DARK_RED = (128, 0, 0)
DARK_GREEN = (0, 128, 0)
DARK_BLUE = (0, 0, 128)

YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)

DARK_YELLOW = (128, 128, 0)
DARK_CYAN = (0, 128, 128)
DARK_PURPLE = (128, 0, 128)


class Vector2:
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y


class Ray:
    def __init__(self, start_pos: Vector2, direction: Vector2):
        self.pos = start_pos
        self.dir = direction
        self.map = Vector2(int(self.pos.x), int(self.pos.y))

        self.delta_dist = Vector2(0, 0)

        if self.dir.y == 0:
            self.delta_dist.x = 0
        elif self.dir.x == 0:
            self.delta_dist.x = 1
        else:
            self.delta_dist.x = abs(1/self.dir.x)

        if self.dir.x == 0:
            self.delta_dist.y = 0
        elif self.dir.y == 0:
            self.delta_dist.y = 1
        else:
            self.delta_dist.y = abs(1/self.dir.y)

        self.step = Vector2(0, 0)
        self.side_dist = Vector2(0, 0)

        if self.dir.x < 0:
            self.step.x = -1
            self.side_dist.x = (self.pos.x - self.map.x) * self.delta_dist.x
        else:
            self.step.x = 1
            self.side_dist.x = (self.map.x + 1.0 - self.pos.x) * self.delta_dist.x

        if self.dir.y < 0:
            self.step.y = -1
            self.side_dist.y = (self.pos.y - self.map.y) * self.delta_dist.y
        else:
            self.step.y = 1
            self.side_dist.y = (self.map.y + 1.0 - self.pos.y) * self.delta_dist.y

    def cast(self, level: np.ndarray) -> int:
        while True:
            if self.side_dist.x < self.side_dist.y:
                self.side_dist.x += self.delta_dist.x
                self.map.x += self.step.x
                side = 0
            else:
                self.side_dist.y += self.delta_dist.y
                self.map.y += self.step.y
                side = 1

            if level[self.map.x, self.map.y] > 0:
                return side


class Player:

    def __init__(self, height: float, start_pos: Vector2, fov: float = 66,
                 move_speed: float = 5.0, rotation_speed: float = 3.0):
        self.height = height
        self.pos = start_pos
        self.fov = fov
        self.dir = Vector2(-1, 0)
        self.plane = Vector2(0, round(fov / 100, 2))
        self.move_speed = move_speed
        self.rotation_speed = rotation_speed

    def move_forward(self, world_map: np.ndarray) -> None:
        if self.front_collision_check_x(world_map):
            self.pos.x += self.dir.x * self.move_speed
        if self.front_collision_check_y(world_map):
            self.pos.y += self.dir.y * self.move_speed

    def move_backward(self, world_map: np.ndarray) -> None:
        if self.back_collision_check_x(world_map):
            self.pos.x -= self.dir.x * self.move_speed
        if self.back_collision_check_y(world_map):
            self.pos.y -= self.dir.y * self.move_speed

    def strafe_left(self, world_map: np.ndarray) -> None:
        pass

    def strafe_right(self, world_map: np.ndarray) -> None:
        pass

    def rotate_left(self) -> None:
        old_dir_x = self.dir.x
        self.dir.x = self.dir.x * math.cos(-self.rotation_speed) - self.dir.y * math.sin(-self.rotation_speed)
        self.dir.y = old_dir_x * math.sin(-self.rotation_speed) + self.dir.y * math.cos(-self.rotation_speed)
        old_plane_x = self.plane.x
        self.plane.x = self.plane.x * math.cos(-self.rotation_speed) - self.plane.y * math.sin(-self.rotation_speed)
        self.plane.y = old_plane_x * math.sin(-self.rotation_speed) + self.plane.y * math.cos(-self.rotation_speed)

    def rotate_right(self) -> None:
        old_dir_x = self.dir.x
        self.dir.x = self.dir.x * math.cos(self.rotation_speed) - self.dir.y * math.sin(self.rotation_speed)
        self.dir.y = old_dir_x * math.sin(self.rotation_speed) + self.dir.y * math.cos(self.rotation_speed)
        old_plane_x = self.plane.x
        self.plane.x = self.plane.x * math.cos(self.rotation_speed) - self.plane.y * math.sin(self.rotation_speed)
        self.plane.y = old_plane_x * math.sin(self.rotation_speed) + self.plane.y * math.cos(self.rotation_speed)

    def update(self) -> None:
        pass

    def front_collision_check_x(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos.x + self.dir.x * self.move_speed), int(self.pos.y)]

    def front_collision_check_y(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos.x), int(self.pos.y + self.dir.y * self.move_speed)]

    def back_collision_check_x(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos.x - self.dir.x * self.move_speed), int(self.pos.y)]

    def back_collision_check_y(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos.x), int(self.pos.y - self.dir.y * self.move_speed)]


class PlayerCommand:
    def execute(self, player: Player) -> None:
        pass


class PlayerMoveCommand:
    def execute(self, player: Player, world_map: np.ndarray) -> None:
        pass


class MoveForwardCommand(PlayerMoveCommand):
    def execute(self, player: Player, world_map: np.ndarray) -> None:
        player.move_forward(world_map)


class MoveBackwardCommand(PlayerMoveCommand):
    def execute(self, player: Player, world_map: np.ndarray) -> None:
        player.move_backward(world_map)


class StrafeLeftCommand(PlayerMoveCommand):
    def execute(self, player: Player, world_map: np.ndarray) -> None:
        player.strafe_left(world_map)


class StrafeRightCommand(PlayerMoveCommand):
    def execute(self, player: Player, world_map: np.ndarray) -> None:
        player.strafe_right(world_map)


class RotateLeftCommand(PlayerCommand):
    def execute(self, player: Player) -> None:
        player.rotate_left()


class RotateRightCommand(PlayerCommand):
    def execute(self, player: Player) -> None:
        player.rotate_right()


class InputHandler:
    def handle_input(self) -> List:
        """
        return a list of instances of PlayerCommand objects
        the PlayerCommands can be executed by iterating over the returned list and calling execute(player)
        on each PlayerCommand object, assuming "player" is an instance of a Player object
        :return:
        """

        player_commands = []

        for event in pygame.event.get():
            # if the escape key is pressed or the window is closed, end the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                sys.exit()

            # process key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_commands.append(RotateLeftCommand())
                if event.key == pygame.K_RIGHT:
                    player_commands.append(RotateRightCommand())
                if event.key == pygame.K_a:
                    player_commands.append(StrafeLeftCommand())
                if event.key == pygame.K_d:
                    player_commands.append(StrafeRightCommand())
                if event.key == pygame.K_w:
                    player_commands.append(MoveForwardCommand())
                if event.key == pygame.K_s:
                    player_commands.append(MoveBackwardCommand())

        return player_commands


class Framebuffer:
    pass


class WorldMap:
    def __init__(self, world_map: np.ndarray):
        self.array = world_map

    def cast_ray(self, ray: Ray):
        pass


sample_level = np.array([
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


def run_game(screen_width: int, screen_height: int, updates_per_second: int,
             level: np.ndarray = sample_level, screen_title: str = "Raycasting") -> None:
    # create the game variables
    pygame.init()

    screen_size = screen_width, screen_height

    screen = pygame.display.set_mode(screen_size, flags=pygame.SCALED)
    pygame.display.set_caption(screen_title)

    pixels = pygame.PixelArray(screen)

    handler = InputHandler()

    player = Player(screen_height / 2, Vector2(22, 12))

    previous_time = time.perf_counter()
    lag = 0.0
    update_rate = int(1000 / updates_per_second)
    clock = pygame.time.Clock()

    while True:
        # current_time = time.perf_counter()
        # elapsed_time = current_time - previous_time
        # previous_time = current_time
        # lag += elapsed_time

        # ***********************
        # BEGIN PROCESSING INPUT

        commands = handler.handle_input()

        # FINISH PROCESSING INPUT
        # ***********************

        while lag >= update_rate:
            # ******************************
            # BEGIN UPDATING THE GAME STATE

            for command in commands:
                if isinstance(command, PlayerCommand):
                    command.execute(player)
                elif isinstance(command, PlayerMoveCommand):
                    command.execute(player, level)

            # pygame.time.wait(update_rate)

            # lag -= update_rate

            # FINISH UPDATING THE GAME STATE
            # ******************************
            break

        # *************************
        # BEGIN RENDERING THE GAME

        screen.fill(BLACK)

        for pixel_col in range(screen_width):

            camera_x = oh.get_camera_x(pixel_col, screen_width)
            ray_dir = oh.get_ray_dir_vector(player.dir, player.plane, camera_x)
            ray = Ray(player.pos, ray_dir)
            side = ray.cast(level)

            if side == 0:
                perpendicular_wall_dist = (ray.map.x - player.pos.x + (1 - ray.step.x) / 2) / ray.dir.x
            else:
                perpendicular_wall_dist = (ray.map.y - player.pos.y + (1 - ray.step.y) / 2) / ray.dir.y

            try:
                line_height = int(screen_height / perpendicular_wall_dist)
            except ZeroDivisionError:
                line_height = screen_height

            draw_start = int(-line_height / 2 + screen_height / 2)
            if draw_start < 0:
                draw_start = 0

            draw_end = int(line_height / 2 + screen_height / 2)
            if draw_end >= screen_height:
                draw_end = screen_height - 1

            if level[ray.map.x, ray.map.y] == 1:
                if side == 0:
                    color = RED  # red
                else:
                    color = DARK_RED
            elif level[ray.map.x, ray.map.y] == 2:
                if side == 0:
                    color = GREEN  # green
                else:
                    color = DARK_GREEN
            elif level[ray.map.x, ray.map.y] == 3:
                if side == 0:
                    color = BLUE  # blue
                else:
                    color = DARK_BLUE
            elif level[ray.map.x, ray.map.y] == 4:
                if side == 0:
                    color = WHITE  # white
                else:
                    color = GRAY
            else:
                if side == 0:
                    color = YELLOW  # yellow
                else:
                    color = DARK_YELLOW

            for pixel_row in range(draw_start, draw_end):
                pixels[pixel_col][pixel_row] = color

        pygame.display.flip()

        # FINISH RENDERING THE GAME
        # *************************

        clock.tick()


def main():
    run_game(128, 100, 1)


if __name__ == "__main__":
    main()
