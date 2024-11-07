# utils/cube.py
import numpy as np
from typing import List, Tuple


class MagicCube:
    def __init__(self, size: int = 5, alpha: int = 0):
        self.size = size
        self.cube = self.initialize_cube()
        self.magic_number = self.calculate_ideal_magic_number()
        self.alpha = alpha


    def initialize_cube(self) -> np.ndarray:
        n3 = self.size ** 3
        numbers = np.random.permutation(n3) + 1
        return numbers.reshape((self.size, self.size, self.size))

    def calculate_ideal_magic_number(self) -> float:
        n3 = self.size ** 3
        return (self.size * (n3 + 1)) // 2

    def swap(self, pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]):
        i1, j1, k1 = pos1
        i2, j2, k2 = pos2
        self.cube[i1, j1, k1], self.cube[i2, j2, k2] = \
            self.cube[i2, j2, k2], self.cube[i1, j1, k1]

    def get_row_sum(self, i: int, j: int) -> float:
        return np.sum(self.cube[i, j, :])

    def get_column_sum(self, i: int, j: int) -> float:
        return np.sum(self.cube[:, i, j])

    def get_pillar_sum(self, i: int, j: int) -> float:
        return np.sum(self.cube[i, :, j])

    def get_space_diagonals(self) -> List[float]:
        diagonals = []
        n = self.size
        diagonals.append(np.sum([self.cube[i, i, i] for i in range(n)]))
        diagonals.append(np.sum([self.cube[i, i, n - 1 - i] for i in range(n)]))
        diagonals.append(np.sum([self.cube[i, n - 1 - i, i] for i in range(n)]))
        diagonals.append(np.sum([self.cube[i, n - 1 - i, n - 1 - i] for i in range(n)]))
        return diagonals

    def get_plane_diagonals(self) -> List[float]:
        diagonals = []
        n = self.size
        for i in range(n):
            diagonals.append(np.sum([self.cube[i, j, j] for j in range(n)]))
            diagonals.append(np.sum([self.cube[i, j, n - 1 - j] for j in range(n)]))
            diagonals.append(np.sum([self.cube[j, i, j] for j in range(n)]))
            diagonals.append(np.sum([self.cube[j, i, n - 1 - j] for j in range(n)]))
            diagonals.append(np.sum([self.cube[j, j, i] for j in range(n)]))
            diagonals.append(np.sum([self.cube[j, n - 1 - j, i] for j in range(n)]))
        return diagonals

    def calculate_objective_function(self) -> float:
        total_deviation = 0
        n = self.size

        # Accumulate deviations for rows, columns, and pillars
        for i in range(n):
            for j in range(n):
                total_deviation += abs(self.get_row_sum(i, j) - self.magic_number)
                total_deviation += abs(self.get_column_sum(i, j) - self.magic_number)
                total_deviation += abs(self.get_pillar_sum(i, j) - self.magic_number)

        # Accumulate deviations for space and plane diagonals
        for d_sum in self.get_space_diagonals():
            total_deviation += abs(d_sum - self.magic_number)
        for d_sum in self.get_plane_diagonals():
            total_deviation += abs(d_sum - self.magic_number)

        # Normalize deviation to fit within the expected range
        normalized_deviation = (total_deviation / 109)

        # Calculate correct sums and apply alpha scaling
        correct_sums = sum(1 for x in self.get_space_diagonals() if x == self.magic_number) + \
                       sum(1 for x in self.get_plane_diagonals() if x == self.magic_number)
        objective_value = -normalized_deviation + (self.alpha * correct_sums)

        # Enforce the limit to not exceed -109
        return max(objective_value, -109)
    def copy(self) -> 'MagicCube':
        new_cube = MagicCube(self.size)
        new_cube.cube = self.cube.copy()
        return new_cube
