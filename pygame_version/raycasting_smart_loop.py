import math
import pygame
import sys
import numpy as np
import helpers as helper
import time
from typing import List, Union


class Vector2:
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y


class Ray:
    def __init__(self, start_pos: Vector2, direction: Vector2):
        self.pos = start_pos
        self.dir = direction


class Player:

    def __init__(self, height: float, pos_x: int, pos_y: int, fov: float = 66,
                 move_speed: float = 1.0, rotation_speed: float = 1.0):
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.fov = fov
        self.dir_x = -1
        self.dir_y = 0
        self.plane_x = 0
        self.plane_y = 1 / fov
        self.move_speed = move_speed
        self.rotation_speed = rotation_speed

    def move_forward(self, world_map: np.ndarray) -> None:
        if self.front_collision_check_x(world_map):
            self.pos_x += self.dir_x * self.move_speed
        if self.front_collision_check_y(world_map):
            self.pos_y += self.dir_y * self.move_speed

    def move_backward(self, world_map: np.ndarray) -> None:
        if self.back_collision_check_x(world_map):
            self.pos_x -= self.dir_x * self.move_speed
        if self.back_collision_check_y(world_map):
            self.pos_y -= self.dir_y * self.move_speed

    def strafe_left(self, world_map: np.ndarray) -> None:
        pass

    def strafe_right(self, world_map: np.ndarray) -> None:
        pass

    def rotate_left(self) -> None:
        old_dir_x = self.dir_x
        self.dir_x = self.dir_x * math.cos(-self.rotation_speed) - self.dir_y * math.sin(-self.rotation_speed)
        self.dir_y = old_dir_x * math.sin(-self.rotation_speed) + self.dir_y * math.cos(-self.rotation_speed)
        old_plane_x = self.plane_x
        self.plane_x = self.plane_x * math.cos(-self.rotation_speed) - self.plane_y * math.sin(-self.rotation_speed)
        self.plane_y = old_plane_x * math.sin(-self.rotation_speed) + self.plane_y * math.cos(-self.rotation_speed)

    def rotate_right(self) -> None:
        old_dir_x = self.dir_x
        self.dir_x = self.dir_x * math.cos(self.rotation_speed) - self.dir_y * math.sin(self.rotation_speed)
        self.dir_y = old_dir_x * math.sin(self.rotation_speed) + self.dir_y * math.cos(self.rotation_speed)
        old_plane_x = self.plane_x
        self.plane_x = self.plane_x * math.cos(self.rotation_speed) - self.plane_y * math.sin(self.rotation_speed)
        self.plane_y = old_plane_x * math.sin(self.rotation_speed) + self.plane_y * math.cos(self.rotation_speed)

    def update(self) -> None:
        pass

    def front_collision_check_x(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos_x + self.dir_x * self.move_speed), int(self.pos_y)]

    def front_collision_check_y(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos_x), int(self.pos_y + self.dir_y * self.move_speed)]

    def back_collision_check_x(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos_x - self.dir_x * self.move_speed), int(self.pos_y)]

    def back_collision_check_y(self, world_map: np.ndarray) -> bool:
        return not world_map[int(self.pos_x), int(self.pos_y - self.dir_y * self.move_speed)]


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
    def handle_input(self) -> List[Union[None, PlayerCommand]]:
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

    def cast_ray(self, ray_start_x: float, ray_start_y: float, ray_dir_x: float, ray_dir_y: float):
        pass


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


def run_game(updates_per_second: int) -> None:
    # create the game variables
    handler = InputHandler()
    player = Player()

    previous_time = time.perf_counter()
    lag = 0.0
    update_rate = 1 / updates_per_second

    while True:
        current_time = time.perf_counter()
        elapsed_time = current_time - previous_time
        previous_time = current_time
        lag += elapsed_time

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
                    command.execute(player, world_map)

            # FINISH UPDATING THE GAME STATE
            # ******************************
            pass

        # *************************
        # BEGIN RENDERING THE GAME

        pygame.display.flip()

        # FINISH RENDERING THE GAME
        # *************************


def main():
    pass


if __name__ == "__main__":
    main()
