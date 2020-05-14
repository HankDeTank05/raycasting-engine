import numpy as np
import worldmap
import arcade

class Minimap:
    """
    A class representing the minimap for the game

    Contains a 2d list of the same size as the game's map

    Instead of numbers, the elements are boolean values. This keeps track of what the player has seen before (denoted by True) and what the player has not seen before (denoted by False).

    This minimap only draws what the player has seen before, and the player's position within the map
    """

    def __init__(self, map: list, pos_x: int, pos_y: int, floor_color=None, ceiling_color=None, wall_color=None):
        self.minimap = np.array(map)

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.floor_color = floor_color
        self.ceiling_color = ceiling_color
        self.wall_color = wall_color

        self.player_x = None
        self.player_y = None

        self.x_size = len(self.minimap[0])
        self.y_size = len(self.minimap)

        self.changed = False

        for i in range(len(self.minimap)):
            for j in range(len(self.minimap[i])):
                if i != 0 and j != 0 and i != len(self.minimap)-1 and j != len(self.minimap[i])-1:
                    self.minimap[i][j] = False
                else:
                    self.minimap[i][j] = True

        self.shape_list = arcade.ShapeElementList()

        floor = arcade.create_rectangle_filled(self.pos_x, self.pos_y, self.x_size, self.y_size, self.floor_color)

        self.shape_list.append(floor)

        self.revealed_wall_point_list = []

    def __str__(self):
        output = ''
        for i in range(len(self.minimap)):
            for j in range(len(self.minimap[i])):
                if self.minimap[i, j] > 0:
                    output += f'{self.minimap[i, j]} '
                else:
                    output += '  '
            output += '\n'
        return output

    def update_walls(self, update_points: list):
        """takes a list of (x, y) tuples denoting coordinates of walls in the map that have been seen by the player for the first time"""
        for point in update_points:
            row = point[1]
            col = point[0]
            if row >= 0 and row < self.y_size and col >= 0 and col < self.x_size:
                self.minimap[row, col] = 1
                self.changed = True
                self.revealed_wall_point_list.append((col, row))  # append a tuple for the wall point to the list, in the form of (x_loc, y_loc)

    def update_player_pos(self, player_x, player_y):
        if self.player_x is not None and self.player_y is not None:
            self.minimap[self.player_y, self.player_x] = 0
        self.player_x = player_x
        self.player_y = player_y
        self.minimap[self.player_y, self.player_x] = 2
        self.changed = True

    def draw(self):
        if self.changed:
            #print(self)
            self.shape_list.draw()
            self.changed = False
        else:
            return


if __name__ == "__main__":
    test_map = worldmap.Maze(10, 10)
    test_map.generate_with_recursive_backtracking(0, 0)
    raycasting_map = test_map.get_map_for_raycasting()
    test_minimap = Minimap(raycasting_map, 1, 1)
    print("Here's the minimap")
    #print(len(test_minimap.minimap))
    print(test_minimap)
    test_minimap.update_walls([(10, 10), (11, 11), (10, 15)])
    test_minimap.draw()
