import numpy as np
import random


class Cell:
    """
    A class representing one cell on the map
    """

    def __init__(self, pos_x: int, pos_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.visited = False

    def __repr__(self):
        if self.visited:
            visit_status = 'Visited'
        else:
            visit_status = 'Unvisited'
        return f'{visit_status} cell at ({self.pos_x}, {self.pos_y})'

    def __str__(self):
        return 'C'


class RectangularMap:
    """
    A class representing the world map the player will walk around in
    """

    def __init__(self, cell_width: int, cell_height: int, open_map=True):
        # cell width/height is the measure of how wide/high the map is
        # in terms of the NUMBER OF CELLS
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_map = []

        # generate the cell map. each cell's data is the value of the given cell
        for h in range(self.cell_height):
            self.cell_map.append([])
            for w in range(self.cell_width):
                new_cell = Cell(0)
                self.cell_map[h].append(new_cell)

        # map width/height is the measure of how wide/high the LIST REPRESENTATION of the map is
        # this is in terms of the NUMBER OF INDICES IN THE LIST REPRESENTATION of the map
        self.list_rep_width = abs(cell_width * 2) + 1
        self.list_rep_height = abs(cell_height * 2) + 1
        self.list_rep = []

        for h in range(self.list_rep_height):
            self.list_rep.append([])
            for w in range(self.list_rep_width):
                self.list_rep[h].append(22)

        self.update_list_rep()

    def __repr__(self):
        pass

    def update_list_rep(self):
        for h in range(self.list_rep_height):
            cell_h = (h - 1) / 2
            for w in range(self.list_rep_width):
                cell_w = (w - 1) / 2

                # if we're at a cell's location in the list_rep list
                if cell_w % 1 == 0 and cell_h % 1 == 0:
                    # append the cell's data to the list
                    self.list_rep[h][w] = self.cell_map[int(cell_h)][int(cell_w)]
                    if self.list_rep[h][w].has_right():
                        self.list_rep[h][w + 1] = '  '
                    else:
                        self.list_rep[h][w + 1] = 'xx'
                    if self.list_rep[h][w].has_down():
                        self.list_rep[h - 1][w] = '  '
                    else:
                        self.list_rep[h - 1][w] = 'xx'

    def print_cell_map(self):
        for h in self.cell_map:
            print(h)

    def print_list_rep(self):
        for h in self.list_rep:
            for w in h:
                print(f'{w} ', end='')
            print()

    def mazify(self, cell_start_x: int, cell_start_y: int):
        # generate the maze
        mazify = Maze(self.cell_width, self.cell_height, cell_start_x, cell_start_y, 0, 0)
        self.cell_map = mazify.cells
        # update the list representation of the map
        self.update_list_rep()


class Maze:
    def __init__(self, x_size: int, y_size: int):
        self.width = x_size*2 + 1
        self.height = y_size*2 + 1
        self.maze = []

        for i in range(self.height):
            self.maze.append([])
            for j in range(self.width):
                if i % 2 == 1 and j % 2 == 1:
                    self.maze[i].append(Cell(j//2, i//2))
                elif i == 0 or i == self.height-1 or j == 0 or j == self.width-1:
                    self.maze[i].append('X')
                else:
                    self.maze[i].append(1)
            # print(self.maze[i])

    def generate_with_recursive_backtracking(self, start_cell_x: int, start_cell_y: int):
        stack = []

        while len(stack) > 0:
            stack.pop()
            pass
        pass

    def __str__(self):
        return_string = ''
        for row in self.maze:
            return_string += str(row) + '\n'

        return return_string


if __name__ == "__main__":
    test_maze = Maze(5,5)
