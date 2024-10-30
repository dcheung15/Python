import random
import numpy as np
import pygame
import shape
from collision import CollisionDetector
from ground import Ground
from tiles import Tile

class Board:

    def __init__(self, screen, height=24, width=10):
        self.height = height
        self.width = width
        self.screen = screen
        self.ground = Ground(width, height)
        self._collision_detector = CollisionDetector(self, self.ground)
        self._matrix = np.zeros([width, height], dtype=int)
        self._current_tile = None
        self.score = 0
        self.colors = shape.generate_colors()
        self.shapes = shape.generate_shapes()

    def draw(self):
        block_size = 35  # Set the size of the grid block
        x_offset = 100
        y_offset = 50
        for x in range(0, self.width):
            for y in range(0, self.height):
                rect = pygame.Rect(x_offset + x * block_size, y_offset + y * block_size, block_size, block_size)
                pygame.draw.rect(self.screen, self.colors[self._matrix[x, y]], rect, 1 if self._matrix[x, y] == 0 else 0)

    # updates the board by moving the tile or creating the tile
    def update(self, on_timer=True):
        if self._current_tile is None:
            self.create_tile()
        if on_timer:
            self.drop_tile()

        self._matrix[:, :] = 0
        self.draw_tile(self._current_tile)
        self.drawground(self.ground)

    # locks the tiles when they make collision with ground and merges it to the ground
    def drop_tile(self):
        is_locked = self._current_tile.move(0, 1)
        if is_locked:
            self.ground.merge(self._current_tile)
            self.score = self.score + self.ground.expire_rows()  # check for completed rows
            self.create_tile()

    def create_tile(self):
        self._current_tile = Tile(self._collision_detector, self.get_shape(), self.get_color(), random.randint(0, 6))

    def get_shape(self):
        return self.shapes[random.randint(0, len(self.shapes) - 1)]

    def get_color(self):
        return random.randint(1, len(self.colors) - 1)

    def draw_tile(self, tile):
        matrix = tile.get_coordinates()
        for pos in matrix:
            if pos[1] < self.height:
                self._matrix[pos[0], pos[1]] = tile.get_color()

    def drawground(self, ground):
        self._matrix = np.maximum(self._matrix, ground.get_matrix())

    def on_key_up(self):
        self._current_tile.rotate(1)
        self.draw()

    def on_key_down(self):
        self._current_tile.move(0, 1)
        self.draw()

    def on_key_left(self):
        self._current_tile.move(-1, 0)
        self.draw()

    def on_key_right(self):
        self._current_tile.move(1, 0)
        self.draw()
