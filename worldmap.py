import numpy as np
import random
import copy
import csv

def scale_up_2d_list(lst: list, scale_factor: int):
    scaled_list = np.array(lst)
    scaled_list = np.repeat(scaled_list, scale_factor, axis=1)
    scaled_list = np.repeat(scaled_list, scale_factor, axis=0)
    return scaled_list

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
    def __init__(self, cell_size_x: int, cell_size_y: int):
        self.cell_width = cell_size_x
        self.cell_height = cell_size_y
        self.width = cell_size_x * 2 + 1
        self.height = cell_size_y * 2 + 1
        self.maze = []

        for i in range(self.height):
            self.maze.append([])
            for j in range(self.width):
                if i % 2 == 1 and j % 2 == 1:
                    self.maze[i].append(Cell(j//2, i//2, j, i))
                elif i == 0 or i == self.height-1 or j == 0 or j == self.width-1:
                    self.maze[i].append('X')
                else:
                    self.maze[i].append(1)
            # print(self.maze[i])

    def generate_with_recursive_backtracking(self, start_cell_x: int, start_cell_y: int):
        def neighbor_checker(x: int, y: int):
            """
            checks all the neighbor cells for ones that have not been visited,
            and returns the coordinates of the unvisited ones
            :param x:
            :param y:
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

        pass

    def get_map_for_raycasting(self):
        output = []
        for i in range(len(self.maze)):
            output.append([])
            for j in range(len(self.maze[i])):
                current_element = self.maze[i][j]
                if isinstance(current_element, str):
                    if current_element == 'X':
                        output[i].append(1)
                    elif current_element == ' ':
                        output[i].append(0)
                elif not isinstance(current_element, int):
                    output[i].append(0)
                else:
                    output[i].append(1)
        return scale_up_2d_list(output, 2)

    def output_maze_to_csv(self, filename: str = 'maze.csv'):
        with open(filename, mode='w') as mazefile:
            mazefile = csv.writer(mazefile)

            for row in self.maze:
                mazefile.writerow(row)

    def __str__(self):
        return_string = ''
        for row in self.maze:
            for cell in row:
                return_string += str(cell) + ' '
            return_string += '\n'

        return return_string


if __name__ == "__main__":
    test_maze = Maze(30, 30)
    print(test_maze)
    test_maze.generate_with_recursive_backtracking(0, 0)
    print(test_maze)
    #raycasting_maze = test_maze.get_map_for_raycasting()
    #print(raycasting_maze)
    test_maze.output_maze_to_csv()
