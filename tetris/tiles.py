import numpy as np
from collision import Collision

class Tile:

    def __init__(self, collision_detector, shape, color, pos_x=5, pos_y=0, rotation=0):
        self.shape = shape
        self.rotation = rotation
        self.color = color
        self.position = np.array([pos_x, pos_y])
        self.collision_detector = collision_detector
        self.is_locked = False

    def render(self, board):
        matrix = self.get_coordinates()
        board.draw_tile(matrix, self.color)

    def get_coordinates(self):
        return self.shape.get_matrix_with_offset(self.rotation, self.position)

    def get_color(self):
        return self.color

    def rotate(self, direction):
        new_rotation = np.abs(np.mod(self.rotation + direction, self.shape.rotations_count))
        new_matrix = self.shape.get_matrix_with_offset(new_rotation, self.position)
        collision = self.collision_detector.check(new_matrix, 0, 0)
        if collision is Collision.BOTTOM:
            self.is_locked = True
        if collision is Collision.NONE:
            self.rotation = new_rotation

    def move(self, dx, dy):
        next_pos = self.position + np.array([dx, dy])
        new_matrix = self.shape.get_matrix_with_offset(self.rotation, next_pos)
        collision = self.collision_detector.check(new_matrix, dx, dy)
        if collision == Collision.BOTTOM:
            self.is_locked = True
        if collision is Collision.NONE:
            self.position = next_pos
        return self.is_locked
