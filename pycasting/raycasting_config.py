import arcade
import numpy as np


class ColorScheme:
    """
    A class that contains all of the colors for a given color scheme
    """

    def __init__(self, floor=arcade.color.LAWN_GREEN, ceiling=arcade.color.DEEP_SKY_BLUE,
                 numbers=[], numbers_dark=[]):
        self.scheme = {
            'floor': floor,
            'ceiling': ceiling,
            'numbers': numbers,
            'numbers_dark': numbers_dark
        }

    def edit(self, parameter, color):
        self.scheme[parameter] = color

    def set_floor(self, color):
        self.scheme['floor'] = color

    def set_ceiling(self, color):
        self.scheme['ceiling'] = color

    def set_numbered_colors(self, colors: list):
        self.scheme['numbers'] = colors

    def set_numbered_dark_colors(self, colors: list):
        if len(colors) == len(self.scheme['numbers']):
            self.scheme['numbers_dark'] = colors


class WorldMap:
    """
    A class representing the world map for a stage
    """

    def __init__(self, width, length):
        self.map = [length][width]

    def __repr__(self):
        output = ''
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                output += f'{self.map[y][x]} '
            output += '\n'
        return output

    def mimic_2d_list(self, mimic: list):
        pass
