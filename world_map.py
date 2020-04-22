class WorldMap:

    def __init__(self, size_x, size_y):
        self.map = []
        for y in range(size_y):
            self.map.append([])
            for x in range(size_x):
                self.map[y].append([])
        self.width = size_x
        self.height = size_y

    def visualize(self):
        for y in range(len(self.map)):
            row = ''
            for x in range(len(self.map[y])):
                row += f'{x},{self.height-y-1}\t'
            print(row)
            print()

    def erase_and_populate_manually(self):
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                if len(self.map[y][x])

if __name__ == "__main__":
    testmap = WorldMap(5, 5)
    testmap.visualize()
