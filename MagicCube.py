import random

class MagicCube:
    def __init__(self):
        self.size = 5
        self.cube = self.create_random_cube()
        self.magic_number = 315  # sum of each line should be 315

    def create_random_cube(self):
        numbers = list(range(1, 126))  # 1 to 125 for 5x5x5 cube
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
        
        # Check rows (75 lines)
        for i in range(self.size):
            for j in range(self.size):
                # rows in xy-plane
                if sum(cube[i][j]) == self.magic_number:
                    value += 1
                # rows in xz-plane
                if sum(cube[i][k][j] for k in range(self.size)) == self.magic_number:
                    value += 1
                # rows in yz-plane
                if sum(cube[k][i][j] for k in range(self.size)) == self.magic_number:
                    value += 1

        # Check diagonals in each 2D plane (15 planes * 2 diagonals = 30 lines)
        for i in range(self.size):
            # diagonals in xy-plane
            if sum(cube[i][j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[i][j][self.size-1-j] for j in range(self.size)) == self.magic_number:
                value += 1
            
            # diagonals in xz-plane
            if sum(cube[i][j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[i][self.size-1-j][j] for j in range(self.size)) == self.magic_number:
                value += 1
            
            # diagonals in yz-plane
            if sum(cube[j][i][j] for j in range(self.size)) == self.magic_number:
                value += 1
            if sum(cube[j][i][self.size-1-j] for j in range(self.size)) == self.magic_number:
                value += 1

        # Check space diagonals (4 lines)
        # Main space diagonal
        if sum(cube[i][i][i] for i in range(self.size)) == self.magic_number:
            value += 1
        # Other space diagonals
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

    def get_position_value(self, i, j, k):
        return self.cube[i][j][k]

    def get_successor(self, mode="random"):
        if mode == "random":
            # Get two random positions
            pos1 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
            pos2 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
            while pos1 == pos2:
                pos2 = (random.randint(0, 4), random.randint(0, 4), random.randint(0, 4))
            return self.swap_positions(self.cube, pos1, pos2)
        
        elif mode == "best":
            current_value = self.calculate_value()
            best_value = current_value
            best_cube = self.copy_cube(self.cube)
            best_pos1 = None
            best_pos2 = None
            total_checked = 0
            
            for i1 in range(self.size):
                for j1 in range(self.size):
                    for k1 in range(self.size):
                        for i2 in range(self.size):
                            for j2 in range(self.size):
                                for k2 in range(self.size):
                                    # Skip if same position
                                    if (i1, j1, k1) >= (i2, j2, k2):
                                        continue
                                    
                                    total_checked += 1
                                    # if total_checked % 1000 == 0:
                                    #    print(f"Checked {total_checked} swaps... Current best: {best_value}")
                                    
                                    # swap position
                                    new_cube = self.swap_positions(self.cube, (i1, j1, k1), (i2, j2, k2))
                                    value = self.calculate_value(new_cube)
                                    
                                    if value > best_value:
                                        best_value = value
                                        best_cube = new_cube
                                        best_pos1 = (i1, j1, k1)
                                        best_pos2 = (i2, j2, k2)
                                        # print(f"\nFound better solution!")
                                        # print(f"Swapped positions: ({i1},{j1},{k1}) <-> ({i2},{j2},{k2})")
                                        # print(f"Values swapped: {self.get_position_value(i1,j1,k1)} <-> {self.get_position_value(i2,j2,k2)}")
                                        # print(f"New value: {value}\n")
            
            # print(f"\nSearch completed!")
            # print(f"Total positions checked: {total_checked}")
            # if best_value > current_value:
            #    print(f"Best improvement found: +{best_value - current_value}")
            #    print(f"Final value: {best_value}")
            #    print(f"Best swap: {best_pos1} <-> {best_pos2}")
            # else:
            #    print("No better solution found")
            
            return best_cube

    def print_cube(self):
        print("\nCurrent Cube State:")
        for i in range(self.size):
            print(f"\nLayer {i+1}:")
            for row in self.cube[i]:
                print([f"{x:3d}" for x in row])
        print(f"\nCurrent Value: {self.calculate_value()}")
        if self.calculate_value() == 109:  # Total possible lines that should sum to 315
            print("Congratulations! Magic cube solved!")
        else:
            print("Magic cube not yet solved.")


M = MagicCube()
M.print_cube()

new_cube = M.get_successor("best")
M.cube = new_cube
M.print_cube()