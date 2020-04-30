class ColorLists:
    """
    A class for easily creating a list of colors to use when rendering the walls in the engine
    """

    def __init__(self, colors: list = []):
        self.main_color_list = colors
        self.dark_color_list = None
