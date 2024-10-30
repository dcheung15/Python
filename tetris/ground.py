import numpy as np

class Ground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = np.zeros([width, height], dtype=int)
        self.coordinates = list()

    def merge(self, tile):
        coordinates = tile.get_coordinates()
        for position in coordinates:
            if (self.matrix[position[0], position[1]] != 0) or (position[0] >= self.width) \
                    or (position[1] >= self.height):
                print("ERROR")
            self.matrix[position[0], [position[1]]] = tile.get_color()
            self.coordinates.append(position)

    def get_matrix(self):
        return self.matrix

    def get_coordinates(self):
        return self.coordinates

    def expire_rows(self): # completed rows
        row_count = 0
        for h in np.arange(1, self.height - 1):
            while np.all(self.matrix[:, self.height - h] != 0):     # row elimination/cascade
                self.cascade(self.height - h)
                row_count = row_count + 1
        if row_count != 0:
            self.recompute_coordinates()
        return row_count

    def cascade(self, up_to):   # elimination method
        rows = np.arange(0, up_to)[::-1]
        for h in rows:
            self.matrix[:, h + 1] = self.matrix[:, h]
        self.matrix[:, 0] = 0

    def recompute_coordinates(self):
        self.coordinates.clear()
        for x in np.arange(len(self.matrix)):
            for y in np.arange(len(self.matrix[x])):
                if self.matrix[x][y] != 0:
                    self.coordinates.append(np.array([x, y]))
