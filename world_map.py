import numpy as np


class Map:
    """
    A class representing the world map the player will walk around in
    """

    def __init__(self, width: int, height: int):
        # ensure the width and height are odd integers
        if width % 2 == 0:
            width += 1
        self.width = width
        if height % 2 == 0:
            height += 1
        self.height = height

        # create the map, with border walls (1) on the edges
        self.map = []

        for row in range(self.height):
            self.map.append([])
            for column in range(self.width):
                if row == 0 or column == 0 or row == self.height-1 or column == self.width-1:
                    self.map[row].append(1)
                else:
                    self.map[row].append(0)

    def __repr__(self):
        output = ''
        for row in range(len(self.map)):
            output += f'\n{self.map[row]}'
        return output

