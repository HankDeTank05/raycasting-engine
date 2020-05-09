import numpy as np
import random


class Cell:
    """
    A class representing one cell on the map
    """

    def __init__(self, pos_x: int, pos_y: int, map_x: int, map_y: int):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.map_x = map_x
        self.map_y = map_y
        self.visited = False

    def __repr__(self):
        if self.visited:
            visit_status = 'Visited'
        else:
            visit_status = 'Unvisited'
        return f'{visit_status} cell at ({self.pos_x}, {self.pos_y})'

    def __str__(self):
        return ' '


class RectangularMap:
    """
    A class representing the world map the player will walk around in
    """

    def __init__(self, player_start_x: int, player_start_y: int, cell_width: int, cell_height: int):
        self.start_x = player_start_x
        self.start_y = player_start_y

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.map_width = self.cell_width * 2 + 1
        self.map_height = self.cell_height * 2 + 1

        self.map = []

        for i in range(self.map_height):
            self.map.append([])
            for j in range(self.map_width):
                if i == 0 or i == self.map_height-1 or j == 0 or j == self.map_width-1:
                    self.map.append('X')
                else:
                    self.map.append(' ')

    def generate_maze_recursive_backtracking(self, cell_start_x: int, cell_start_y: int):
        # generate the maze
        new_map = Maze(self.cell_width, self.cell_height)
        new_map.generate_with_recursive_backtracking()

        # save the maze
        self.map = new_map


class Maze:
    def __init__(self, cell_size_x: int, cell_size_y: int):
        # the size of the maze, measured in maze cells
        self.cell_width = cell_size_x
        self.cell_height = cell_size_y

        # the size of the 2d list that stores the maze (maze cells are in odd numbered rows/columns)
        self.width = cell_size_x * 2 + 1
        self.height = cell_size_y * 2 + 1

        # the (soon-to-be) 2d list that contains the maze itself
        self.maze = []

        # generate a placeholder maze
        for i in range(self.height):
            self.maze.append([])
            for j in range(self.width):
                if i % 2 == 1 and j % 2 == 1:
                    self.maze[i].append(Cell(j//2, i//2, j, i))
                elif i == 0 or i == self.height-1 or j == 0 or j == self.width-1:
                    self.maze[i].append('X')
                else:
                    self.maze[i].append(1)

    def generate_with_recursive_backtracking(self, start_cell_x: int, start_cell_y: int):
        """
        generate a maze starting from the cell at the specified cell coordinates, using the following recursive
        backtracking algorithm:

        1. choose the initial cell
        2. mark it as visited
        3. push it to the stack
        4. while the stack is not empty...
            1. pop a cell from the stack and make it the current cell
            2. if the current cell has any neighbors which have not been visited...
                1. push the current cell back onto the stack
                2. randomly choose one of the unvisited neighbors
                3. remove the wall between the current cell and the chosen cell
                4. mark the chosen neighbor cell as visited
                5. push it back onto the stack

        NOTE: this algorithm, although it doesn't actually use recursion to generate the maze, produces a functionally
              identical maze to the true recursive algorithm. This algorithm is optimized to do so without recursion
              in order to avoid the maximum recursion depth. This allows for larger mazes to be generated.

        CREDITS NOTE: this algorithm was copy-pasted from the source, and then edited for clarity
        source: https://en.wikipedia.org/wiki/Maze_generation_algorithm#Recursive_backtracker (as of 5/9/2020)

        :param start_cell_x:
        the x-coordinate of the CELL from which the maze will start
        NOTE: this is NOT THE LIST (self.maze) x-coordinate!!

        :param start_cell_y:
        the y-coordinate of the CELL from which the maze will start
        NOTE: this is NOT THE LIST (self.maze) y-coordinate!!

        :return:
        """
        def neighbor_checker(x: int, y: int):
            """
            checks all the neighbor cells for ones that have not been visited,
            and returns the coordinates of the unvisited ones

            :param x:
            this is the LIST X-COORDINATE of the cell to check. the LIST coordinate is needed, as this method checks the
            immediately surrounding LIST ELEMENTS (above, to the right, below, and to the left)
            NOTE: this is NOT THE CELL X-COORDINATE

            :param y:
            this is the LIST Y-COORDINATE of the cell to check. the LIST coordinate is needed, as this method checks the
            immediately surrounding LIST ELEMENTS (above, to the right, below, and to the left)
            NOTE: this is NOT THE CELL Y-COORDINATE

            :return:
            """
            unv_neigh = []
            # check the above neighbor
            if self.maze[y-1][x] != 'X' and not self.maze[y-2][x].visited:
                unv_neigh.append((x, y - 2, 'u'))
            # check the right neighbor
            if self.maze[y][x+1] != 'X' and not self.maze[y][x+2].visited:
                unv_neigh.append((x + 2, y, 'r'))
            # check the below neighbor
            if self.maze[y+1][x] != 'X' and not self.maze[y+2][x].visited:
                unv_neigh.append((x, y + 2, 'd'))
            # check the left neighbor
            if self.maze[y][x-1] != 'X' and not self.maze[y][x-2].visited:
                unv_neigh.append((x - 2, y, 'l'))

            return unv_neigh
        stack = []
        if 0 <= start_cell_x < self.cell_width and 0 <= start_cell_y < self.cell_height:
            # convert maze coordinates into 2d list coordinates
            start_maze_x = start_cell_x * 2 + 1
            start_maze_y = start_cell_y * 2 + 1
            # mark the starting cell as the current cell
            current_cell = self.maze[start_maze_y][start_maze_x]
            # mark the current cell as visited
            current_cell.visited = True
            # push the current cell to the stack
            stack.append(current_cell)
        else:
            # if one of the given coordinates is out of range, print an error message and return
            print(f'INVALID STARTING COORDINATES\nx={start_cell_x}\ny={start_cell_y}')
            return

        # while the stack is not empty,
        while len(stack) > 0:
            # pop a cell from the stack and make it the current cell
            current_cell = stack.pop()
            # if the current cell has any neighbors which have not been visited
            unvisited_neighbors = neighbor_checker(current_cell.map_x, current_cell.map_y)
            if len(unvisited_neighbors) > 0:
                # push the current cell to the stack
                stack.append(current_cell)
                # choose one of the unvisited neighbors
                chosen_neighbor = random.choice(unvisited_neighbors)
                # remove the wall between the current_cell and the chosen cell
                if chosen_neighbor[2] == 'u':
                    self.maze[current_cell.map_y-1][current_cell.map_x] = ' '
                elif chosen_neighbor[2] == 'r':
                    self.maze[current_cell.map_y][current_cell.map_x+1] = ' '
                elif chosen_neighbor[2] == 'd':
                    self.maze[current_cell.map_y+1][current_cell.map_x] = ' '
                elif chosen_neighbor[2] == 'l':
                    self.maze[current_cell.map_y][current_cell.map_x-1] = ' '

                chosen_neighbor = self.maze[chosen_neighbor[1]][chosen_neighbor[0]]
                chosen_neighbor.visited = True
                stack.append(chosen_neighbor)

    def __str__(self):
        return_string = ''
        for row in self.maze:
            for cell in row:
                return_string += str(cell) + ' '
            return_string += '\n'

        return return_string


if __name__ == "__main__":
    test_maze = Maze(10, 10)
    print(test_maze)
    test_maze.generate_with_recursive_backtracking(0, 0)
    print(test_maze)
