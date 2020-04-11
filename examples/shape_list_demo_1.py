"""
This demo shows the speed of drawing a full grid of squares using no buffering.

For me this takes about 0.850 seconds per frame.

It is slow because we load all the points and all the colors to the card every
time.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.shape_list_demo_1
"""

import arcade
import timeit

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Shape List Demo 1"

SQUARE_WIDTH = 5
SQUARE_HEIGHT = 5
SQUARE_SPACING = 40