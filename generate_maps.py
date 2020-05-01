import random


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.insert(item, 0)

    def dequeue(self):
        return self.queue.pop()

    def size(self):
        return len(self.queue)

    def is_empty(self):
        if len(self.queue) == 0:
            return True
        return False


class Cell:
    def __init__(self, value: int, visited: bool):
        self.value = value
        self.visited = visited
        self.adjacent = None
        self.visited_adjacent = None

    def __repr__(self):
        return str(self.value)

    def set_adjacent(self, adjacent: tuple):
        self.adjacent = adjacent
        self.visited_adjacent = len(self.adjacent)


def generate_maze(size=5, start: tuple = (0, 0)):
    maze = []

    if size % 2 == 0:
        size += 1

    if start[0] >= size or start[1] >= size:
        print('starting coords out of bounds')
        return

    for y in range(size):
        maze.append([])
        for x in range(size):
            print(f'({y}, {x})')
            maze[y].append(Cell(0, False))
            two_vertical = y + 1 <= size - 1 and y - 1 >= 0
            two_horizontal = x + 1 <= size - 1 and x - 1 >= 0
            if two_horizontal and two_vertical:
                maze[y][x].set_adjacent(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)))
            elif two_horizontal and not two_vertical:
                if y == size - 1:
                    maze[y][x].set_adjacent(((y - 1, x), (y, x + 1), (y, x - 1)))
                elif y == 0:
                    maze[y][x].set_adjacent(((y + 1, x), (y, x + 1), (y, x - 1)))
            elif not two_horizontal and two_vertical:
                if x == size - 1:
                    maze[y][x].set_adjacent(((y + 1, x), (y - 1, x), (y, x - 1)))
                elif x == 0:
                    maze[y][x].set_adjacent(((y + 1, x), (y - 1, x), (y, x + 1)))
            else:
                if x == size - 1 and y == size - 1:
                    maze[y][x].set_adjacent(((y - 1, x), (y, x - 1)))
                elif x == 0 and y == size - 1:
                    maze[y][x].set_adjacent(((y - 1, x), (y, x + 1)))
                elif x == size - 1 and y == 0:
                    maze[y][x].set_adjacent(((y + 1, x), (y, x - 1)))
                elif x == 0 and y == 0:
                    maze[y][x].set_adjacent(((y + 1, x), (y, x + 1)))

            if y % 2 == 1 and x % 2 == 1:
                maze[y][x].value = 1
            elif x == 0 or y == 0 or x == size-1 or y == size-1:
                maze[y][x].value = 1

    queue = Queue()
    visited = 0

    for y in range(len(maze)):
        print(maze[y])

    return maze


if __name__ == "__main__":
    generate_maze(24)
