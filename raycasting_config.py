import arcade

class ColorScheme:
    """
    A class that contains all of the colors for a given color scheme
    """
    def __init__(self, floor=arcade.color.LAWN_GREEN, ceiling=arcade.color.DEEP_SKY_BLUE,
                 numbers=[], numbers_dark=[]):
        self.scheme = {
            'floor': floor,
            'ceiling': ceiling,
            'numbers': [],
            'numbers_dark': []
        }

    def edit(self, parameter, color):
        self.scheme[parameter] = color

    def set_floor(self, color):
        self.scheme['floor'] = color

    def set_ceiling(self, color):
        self.scheme['ceiling'] = color

    def set_numbered_colors(self, colors: list):
        self.scheme['numbers'] = colors

    def set_dark_colors(self, colors: list):
        if len(colors) == len(self.scheme['numbers']):
            self.scheme['numbers_dark'] = colors
