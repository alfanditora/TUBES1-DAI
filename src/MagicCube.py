import random

class MagicCube:
    def __init__(self, cube=None):
        if cube is None:
            self.size = 5
            self.cube = self.create_random_cube()
        else:
            self.size = 5
            self.cube = cube
        self.magic_number = 315
        self.value = self.calculate_value()

    def create_random_cube(self):
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

    def calculate_value(self, cube=None):
        if cube is None:
            cube = self.cube
        value = 0
        
        # (75 lines)
        for i in range(self.size):
            for j in range(self.size):
                # xy-plane
                if sum(cube[i][j]) == self.magic_number:
                    value += 1
                # xz-plane
                if sum(cube[i][k][j] for k in range(self.size)) == self.magic_number:
                    value += 1
                # yz-plane
                if sum(cube[k][i][j] for k in range(self.size)) == self.magic_number:
                    value += 1

        # Diagonal bidang (30 lines)
        for i in range(self.size):
            # diagonal xy-plane
            if sum(cube[i][j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[i][j][self.size-1-j] for j in range(self.size)) == self.magic_number:
                value += 1
            
            # diagonal xz-plane
            if sum(cube[i][j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[i][self.size-1-j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            
            # diagonal yz-plane
            if sum(cube[j][i][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[j][i][self.size-1-j] for j in range(self.size)) == self.magic_number:
                value += 1

        # Diagonal ruang (4 lines)
        if sum(cube[i][i][i] for i in range(self.size)) == self.magic_number:
            value += 1
        if sum(cube[i][i][self.size-1-i] for i in range(self.size)) == self.magic_number:
            value += 1
        if sum(cube[i][self.size-1-i][i] for i in range(self.size)) == self.magic_number:
            value += 1
        if sum(cube[i][self.size-1-i][self.size-1-i] for i in range(self.size)) == self.magic_number:
            value += 1

        return value

    def copy_cube(self, cube):
        return [[[cube[i][j][k] for k in range(self.size)]
                 for j in range(self.size)]
                 for i in range(self.size)]

    def swap_positions(self, cube, pos1, pos2):
        new_cube = self.copy_cube(cube)
        i1, j1, k1 = pos1
        i2, j2, k2 = pos2
        new_cube[i1][j1][k1], new_cube[i2][j2][k2] = new_cube[i2][j2][k2], new_cube[i1][j1][k1]
        return new_cube

    def get_successor(self, mode="random"):
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
            # best_pos1 = None
            # best_pos2 = None
            # total_checked = 0
            
            for i in range(125):
                for j in range(i + 1, 125):
                                    
                    # total_checked += 1
                                    
                    # swap position
                    new_cube = self.swap_positions(self.cube, ((i // 5) // 5, (i // 5) % 5, i % 5), ((j // 5) // 5, (j // 5) % 5, j % 5))
                    value = self.calculate_value(new_cube)
                                    
                    if value > best_value:
                        best_value = value
                        best_cube = new_cube
                        # best_pos1 = ((i // 5) // 5, (i // 5) % 5, i % 5)
                        # best_pos2 = ((j // 5) // 5, (j // 5) % 5, j % 5)
            
            # print(best_pos1)
            # print(best_pos2)
            return MagicCube(best_cube)

    def print_cube(self):
        print("\nCurrent Cube State:")
        for i in range(self.size):
            print(f"\nLayer {i+1}:")
            for row in self.cube[i]:
                formatted_row = [f"{x:3d}" for x in row]
                print(f"[{', '.join(formatted_row)}]")
        print(f"\nCurrent Value: {self.value}")
        if self.value == 109:
            print("Congratulations! Magic cube solved!")

    def save_state(self, filepath):
        with open(filepath, "a") as file:
            for row in range(self.size):
                for col in range(self.size):
                    for depth in range(self.size):
                        file.write(str(self.cube[row][col][depth]) + " ")
                file.write("\n")
            file.write(f";\n")
    
if __name__ == "__main__":
    M = MagicCube()
    M.print_cube()
    M = M.get_successor("best")
    M.print_cube()