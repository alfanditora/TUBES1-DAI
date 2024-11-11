import random
import json
from typing import List, Tuple, Dict, Optional, Any

class MagicCube(object):
    def __init__(self, cube: Optional[List[List[List[int]]]] = None):
        if cube is None:
            self.size = 5
            self.cube = self.create_random_cube()
        else:
            self.size = 5
            self.cube = cube
        self.magic_number = 315
        self.value = self.calculate_value()

    def create_random_cube(self) -> List[List[List[int]]]:
        numbers = list(range(1, 126))
        random.shuffle(numbers)
        
        cube = []
        index = 0
        for i in range(self.size):
            layer = []
            for j in range(self.size):
                row = []
                for k in range(self.size):
                    row.append(numbers[index])
                    index += 1
                layer.append(row)
            cube.append(layer)
        return cube

    def calculate_value(self, cube: Optional[List[List[List[int]]]] = None) -> int:
        if cube is None:
            cube = self.cube
        value = 0
        
        for i in range(self.size):
            for j in range(self.size):
                if sum(cube[i][j]) == self.magic_number:
                    value += 1
                if sum(cube[i][k][j] for k in range(self.size)) == self.magic_number:
                    value += 1
                if sum(cube[k][i][j] for k in range(self.size)) == self.magic_number:
                    value += 1

        for i in range(self.size):
            if sum(cube[i][j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[i][j][self.size-1-j] for j in range(self.size)) == self.magic_number:
                value += 1
            
            if sum(cube[i][j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[i][self.size-1-j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            
            if sum(cube[j][i][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[j][i][self.size-1-j] for j in range(self.size)) == self.magic_number:
                value += 1

        if sum(cube[i][i][i] for i in range(self.size)) == self.magic_number:
            value += 1
        if sum(cube[i][i][self.size-1-i] for i in range(self.size)) == self.magic_number:
            value += 1
        if sum(cube[i][self.size-1-i][i] for i in range(self.size)) == self.magic_number:
            value += 1
        if sum(cube[i][self.size-1-i][self.size-1-i] for i in range(self.size)) == self.magic_number:
            value += 1

        return value

    def copy_cube(self, cube: List[List[List[int]]]) -> List[List[List[int]]]:
        return [[[cube[i][j][k] for k in range(self.size)]
                 for j in range(self.size)]
                 for i in range(self.size)]

    def swap_positions(self, cube: List[List[List[int]]], 
                      pos1: Tuple[int, int, int], 
                      pos2: Tuple[int, int, int]) -> List[List[List[int]]]:
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
            best_cube = self.copy_cube(self.cube)
            
            for i1 in range(self.size):
                for j1 in range(self.size):
                    for k1 in range(self.size):
                        for i2 in range(self.size):
                            for j2 in range(self.size):
                                for k2 in range(self.size):
                                    if (i1, j1, k1) >= (i2, j2, k2):
                                        continue
                                    
                                    new_cube = self.swap_positions(self.cube, (i1, j1, k1), (i2, j2, k2))
                                    value = self.calculate_value(new_cube)
                                    
                                    if value > best_value:
                                        best_value = value
                                        best_cube = new_cube

            return MagicCube(best_cube)

    def print_cube(self) -> None:
        print("\nCurrent Cube State:")
        for i in range(self.size):
            print(f"\nLayer {i+1}:")
            for row in self.cube[i]:
                formatted_row = [f"{x:3d}" for x in row]
                print(f"[{', '.join(formatted_row)}]")
        print(f"\nCurrent Value: {self.value}")
        if self.value == 109:
            print("Congratulations! Magic cube solved!")
        else:
            print("Magic cube not yet solved.")

    def to_dict(self) -> Dict[str, Any]:
        return {
            'cube': self.cube,
            'value': self.value,
            'size': self.size,
            'magic_number': self.magic_number
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MagicCube':
        cube = cls(data['cube'])
        return cube

    def save_state(self, filename: str) -> None:
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f)

    @classmethod
    def load_state(cls, filename: str) -> 'MagicCube':
        with open(filename, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

if __name__ == "__main__":
    cube = MagicCube()
    print("Initial state:")
    cube.print_cube()
    
    successor = cube.get_successor("best")
    print("\nAfter best successor:")
    successor.print_cube()