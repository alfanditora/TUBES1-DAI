# algorithms/hill_climbing.py
import numpy as np
from typing import Tuple, List
from MagicCube import MagicCube
import logging

logger = logging.getLogger(__name__)


class HillClimbing:
    def __init__(self, cube_size: int = 5, max_iterations: int = 100,
                 max_sideways: int = 100, max_restarts: int = 10,
                 max_neighbors: int = 100):
        self.cube_size = cube_size
        self.max_iterations = max_iterations
        self.max_sideways = max_sideways
        self.max_restarts = max_restarts
        self.max_neighbors = max_neighbors
        self.history = []
        logger.info(f"Initialized HillClimbing with size {cube_size}, max_iterations {max_iterations}")

    def _get_random_positions(self) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        n = self.cube_size
        pos1 = (np.random.randint(n), np.random.randint(n), np.random.randint(n))
        pos2 = (np.random.randint(n), np.random.randint(n), np.random.randint(n))
        while pos1 == pos2:
            pos2 = (np.random.randint(n), np.random.randint(n), np.random.randint(n))
        return pos1, pos2

    def _get_all_neighbors(self, cube: MagicCube) -> List[Tuple[MagicCube, float]]:
        neighbors = []
        n = self.cube_size

        # Instead of checking all combinations, sample random positions
        for _ in range(self.max_neighbors):
            i1, j1, k1 = np.random.randint(0, n, 3)
            i2, j2, k2 = np.random.randint(0, n, 3)
            while (i1, j1, k1) == (i2, j2, k2):
                i2, j2, k2 = np.random.randint(0, n, 3)

            new_cube = cube.copy()
            new_cube.swap((i1, j1, k1), (i2, j2, k2))
            obj_value = new_cube.calculate_objective_function()
            neighbors.append((new_cube, obj_value))

        logger.debug(f"Generated {len(neighbors)} neighbors")
        return neighbors

    def steepest_ascent(self, initial_cube: MagicCube = None) -> Tuple[MagicCube, List[float]]:
        if initial_cube is None:
            current_cube = MagicCube(self.cube_size)
        else:
            current_cube = initial_cube.copy()

        iterations = 0
        self.history = []
        current_value = current_cube.calculate_objective_function()
        self.history.append(current_value)

        logger.info(f"Starting steepest ascent with initial value {current_value}")

        while iterations < self.max_iterations:
            neighbors = self._get_all_neighbors(current_cube)
            best_neighbor, best_value = min(neighbors, key=lambda x: x[1])

            if best_value >= current_value:
                logger.info(f"Local minimum found at iteration {iterations}")
                break

            improvement = current_value - best_value
            logger.info(f"Iteration {iterations}: improvement {improvement:.2f}")

            current_cube = best_neighbor
            current_value = best_value
            self.history.append(current_value)
            iterations += 1

        logger.info(f"Finished after {iterations} iterations, final value: {current_value}")
        return current_cube, self.history

    # ... rest of your hill climbing methods with similar logging ...

    def stochastic(self, initial_cube: MagicCube = None) -> Tuple[MagicCube, List[float]]:

        if initial_cube is None:
            current_cube = MagicCube(self.cube_size)
        else:
            current_cube = initial_cube.copy()

        iterations = 0
        self.history = []
        current_value = current_cube.calculate_objective_function()
        self.history.append(current_value)

        while iterations < self.max_iterations:

            pos1, pos2 = self._get_random_positions()
            neighbor_cube = current_cube.copy()
            neighbor_cube.swap(pos1, pos2)
            neighbor_value = neighbor_cube.calculate_objective_function()

            if neighbor_value < current_value:
                current_cube = neighbor_cube
                current_value = neighbor_value
                self.history.append(current_value)

            iterations += 1

        return current_cube, self.history

    def random_restart(self, hill_climbing_func) -> Tuple[MagicCube, List[float]]:

        best_cube = None
        best_value = float('inf')
        all_history = []

        for _ in range(self.max_restarts):
            initial_cube = MagicCube(self.cube_size)
            final_cube, history = hill_climbing_func(initial_cube)
            final_value = final_cube.calculate_objective_function()

            all_history.extend(history)

            if final_value < best_value:
                best_cube = final_cube
                best_value = final_value

        return best_cube, all_history

    def with_sideways_moves(self, initial_cube: MagicCube = None) -> Tuple[MagicCube, List[float]]:

        if initial_cube is None:
            current_cube = MagicCube(self.cube_size)
        else:
            current_cube = initial_cube.copy()

        iterations = 0
        sideways_moves = 0
        self.history = []
        current_value = current_cube.calculate_objective_function()
        self.history.append(current_value)

        while iterations < self.max_iterations and sideways_moves < self.max_sideways:
            pos1, pos2 = self._get_random_positions()
            neighbor_cube = current_cube.copy()
            neighbor_cube.swap(pos1, pos2)
            neighbor_value = neighbor_cube.calculate_objective_function()

            if neighbor_value < current_value:
                current_cube = neighbor_cube
                current_value = neighbor_value
                sideways_moves = 0
                self.history.append(current_value)
            elif neighbor_value == current_value:
                current_cube = neighbor_cube
                sideways_moves += 1
                self.history.append(current_value)

            iterations += 1

        return current_cube, self.history
