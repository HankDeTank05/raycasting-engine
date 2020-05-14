import numpy as np
class Minmap:
    """
    A class representing the minimap for the game

    Contains a 2d list of the same size as the game's map

    Instead of numbers, the elements are boolean values. This keeps track of what the player has seen before (denoted by True) and what the player has not seen before (denoted by False).

    This minimap only draws what the player has seen before, and the player's position within the map
    """

    def __init__(self, map: list, pos_x: int, pos_y: int):
        self.minimap = map

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.x_size = len(self.minimap[0])
        self.y_size = len(self.minimap)

        self.changed = False

        for i in range(len(self.minimap)):
            for j in range(len(self.minimap[i])):
                self.minimap[i][j] = False

    def update_minimap(self, update_points: list):
        """takes a list of (x, y) tuples denoting coordinates of walls in the map that have been seen by the player for the first time"""
        if row >= 0 and row < self.y_size and col >= 0 and col < self.x_size:
            self.minimap[row][col] = True
            self.changed = True

    def draw(self, player_x: int, player_y: int):
        if self.changed:
            # draw the updated map
            pass
        else:
            return
