import arcade
from arcade_version.raycasting import RaycastingEngine
import worldmap as wm
import minimap as mm


def test_run():
    world_map = wm.Maze(5, 5)
    world_map.generate_with_recursive_backtracking(0, 0)
    game = RaycastingEngine(640, 480, "Raycasting Test", False)
    game.setup((1, 1), (-1, 0), (0, 0.66), world_map.get_map_for_raycasting(), 5.0, 2.0, hide_mouse=False)

    arcade.run()


if __name__ == "__main__":
    test_run()
