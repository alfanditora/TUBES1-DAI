import random
import numpy as np
import json
import logging
from typing import List, Tuple, Optional, Union, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class Position:
    x: int
    y: int
    z: int

class MagicCube:
    def __init__(self, cube: Optional[List[List[List[int]]]] = None):
        self.size = 5
        self.magic_number = 315  
        self.cube = cube if cube is not None else self.create_random_cube()
        self.value = self.calculate_value()
        logger.info(f"Initialized MagicCube with value: {self.value}")

    def create_random_cube(self) -> List[List[List[int]]]:
        numbers = list(range(1, self.size**3 + 1))
        random.shuffle(numbers)
        cube_1d = np.array(numbers)
        cube_3d = cube_1d.reshape((self.size, self.size, self.size))
        return cube_3d.tolist()

    def calculate_value(self, cube: Optional[List[List[List[int]]]] = None) -> int:
        if cube is None:
            cube = self.cube
        value = 0
        cube_np = np.array(cube)
        
        for i in range(self.size):
            for j in range(self.size):
                if np.sum(cube_np[i, j, :]) == self.magic_number:
                    value += 1
                if np.sum(cube_np[i, :, j]) == self.magic_number:
                    value += 1
                if np.sum(cube_np[:, i, j]) == self.magic_number:
                    value += 1

        for i in range(self.size):
            if np.sum([cube_np[i, j, j] for j in range(self.size)]) == self.magic_number:
                value += 1
            if np.sum([cube_np[i, j, self.size-1-j] for j in range(self.size)]) == self.magic_number:
                value += 1
            if np.sum([cube_np[i, j, j] for j in range(self.size)]) == self.magic_number:
                value += 1
            if np.sum([cube_np[i, self.size-1-j, j] for j in range(self.size)]) == self.magic_number:
                value += 1
            if np.sum([cube_np[j, i, j] for j in range(self.size)]) == self.magic_number:
                value += 1
            if np.sum([cube_np[j, i, self.size-1-j] for j in range(self.size)]) == self.magic_number:
                value += 1

        space_diagonals = [
            [cube_np[i, i, i] for i in range(self.size)],
            [cube_np[i, i, self.size-1-i] for i in range(self.size)],
            [cube_np[i, self.size-1-i, i] for i in range(self.size)],
            [cube_np[i, self.size-1-i, self.size-1-i] for i in range(self.size)]
        ]
        
        for diagonal in space_diagonals:
            if sum(diagonal) == self.magic_number:
                value += 1

        return value

    def copy_cube(self, cube: List[List[List[int]]]) -> List[List[List[int]]]:
        return np.array(cube).copy().tolist()

    def swap_positions(self, cube: List[List[List[int]]], pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]) -> List[List[List[int]]]:
        new_cube = self.copy_cube(cube)
        i1, j1, k1 = pos1
        i2, j2, k2 = pos2
        new_cube[i1][j1][k1], new_cube[i2][j2][k2] = new_cube[i2][j2][k2], new_cube[i1][j1][k1]
        return new_cube

    def get_successor(self, mode: str = "random") -> 'MagicCube':
        if mode == "random":
            pos1 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
            pos2 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
            while pos1 == pos2:
                pos2 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
            new_cube = self.swap_positions(self.cube, pos1, pos2)
            return MagicCube(new_cube)
        
        elif mode == "best":
            current_value = self.value
            best_value = current_value
            best_cube = None
            n = self.size ** 3
            cube_1d = np.array(self.cube).flatten()
            
            for i in range(n-1):
                for j in range(i+1, n):
                    pos1 = (i // 25, (i % 25) // 5, i % 5)
                    pos2 = (j // 25, (j % 25) // 5, j % 5)
                    new_cube = self.swap_positions(self.cube, pos1, pos2)
                    value = self.calculate_value(new_cube)
                    if value > best_value:
                        best_value = value
                        best_cube = new_cube
            
            return MagicCube(best_cube if best_cube is not None else self.cube)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def print_cube(self) -> None:
        print("\nCurrent Cube State:")
        for i in range(self.size):
            print(f"\nLayer {i+1}:")
            for row in self.cube[i]:
                formatted_row = [f"{x:3d}" for x in row]
                print(f"[{', '.join(formatted_row)}]")
        print(f"\nCurrent Value: {self.value}/109")
        if self.value == 109:
            print("Congratulations! Magic cube solved!")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'cube': self.cube,
            'value': self.value,
            'size': self.size,
            'magic_number': self.magic_number
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MagicCube':
        return cls(data['cube'])

    def save_state(self, filepath: str) -> None:
        try:
            with open(filepath, "a") as file:
                for row in range(self.size):
                    for col in range(self.size):
                        for depth in range(self.size):
                            file.write(str(self.cube[row][col][depth]) + " ")
                    file.write("\n")
                file.write(";\n")
            logger.info(f"Saved state to {filepath}")
        except Exception as e:
            logger.error(f"Error saving state: {e}")
            raise

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    cube = MagicCube()
    print("Initial state:")
    cube.print_cube()
    successor = cube.get_successor("best")
    print("\nAfter best successor:")
    successor.print_cube()