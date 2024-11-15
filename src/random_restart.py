from MagicCube import MagicCube
import matplotlib.pyplot as plt
import time
from typing import List, Tuple
import os

class random_restart_hill_climbing:
    def __init__(self, max_restarts: int = 10):
        self.list_of_value: List[int] = []
        self.max_restarts = max_restarts
        self.num_restarts = 0
        self.total_iterations = 0
        self.start_time = 0
        self.end_time = 0
        self.filepath = self.make_file("randomrestart")

    def hill_climbing(self, current: MagicCube) -> Tuple[MagicCube, int]:

        iterations = 0
        self.list_of_value.append(current.value)

        while True:
            successor = current.get_successor("best")
            if current.value == 109 or successor.value <= current.value:
                break
            current = successor
            self.list_of_value.append(current.value)
            iterations += 1

            current.save_state(self.filepath)

        return current, iterations

    def run(self) -> None:

        self.start_time = time.time()

        best_cube = MagicCube()
        best_value = best_cube.value

        print(f"Initial state:")
        best_cube.print_cube()
        print(f"Initial value: {best_value}\n")

        while self.num_restarts < self.max_restarts:
            current = MagicCube()  # Random restart
            current, iterations = self.hill_climbing(current)
            self.total_iterations += iterations

            if current.value > best_value:
                best_cube = current
                best_value = current.value

            self.num_restarts += 1

            if best_value == 109:
                break


        self.end_time = time.time()

        print(f"\nFinal state:")
        best_cube.print_cube()
        print(f"\nResults:")
        print(f"Number of restarts: {self.num_restarts}")
        print(f"Total iterations: {self.total_iterations}")
        print(f"Best value found: {best_value}")
        print(f"Time taken: {self.end_time - self.start_time:.2f} seconds")

        self.makePlot()

    def makePlot(self) -> None:

        plt.figure(figsize=(12, 6))
        plt.plot(list(range(len(self.list_of_value))), self.list_of_value)
        plt.title("Magic Cube Value over Iterations (Random Restart Hill Climbing)")
        plt.xlabel("Iteration")
        plt.ylabel("Value")
        plt.grid()
        plt.show()

    def make_file(self, name):
        directory = ".\\save_file"
        os.makedirs(directory, exist_ok=True)
        
        counter = 1
        while True:
            filename = f"{name}{counter}.txt"
            filepath = os.path.join(directory, filename)
            
            if not os.path.exists(filepath):
                break
            counter += 1
        
        return filepath

def run_experiment(num_trials: int = 3) -> None:

    print(f"Running {num_trials} trials of Random Restart Hill Climbing")
    print("-" * 50)

    for trial in range(num_trials):
        print(f"\nTrial {trial + 1}:")
        solver = random_restart_hill_climbing(max_restarts=10)
        solver.run()

if __name__ == "__main__":
    run_experiment()