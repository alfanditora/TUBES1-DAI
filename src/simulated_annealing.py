import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from MagicCube import MagicCube
import os
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

@dataclass
class AnnealingConfig:
    initial_temp: float = 1000000.0
    cooling_rate: float = 0.99995
    min_temp: float = 0.0001
    max_iterations: int = 500000
    stuck_threshold: int = 175000
    num_neighbors: int = 10
    parallel_processing: bool = True
    max_workers: int = 4

class SimulatedAnnealing:
    def __init__(self, initial_temp=1000000.0, cooling_rate=0.99995, min_temp=0.0001, max_iterations=500000):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iterations = max_iterations
        self.objective_values = []
        self.temperatures = []
        self.exp_deltaE_T = []
        self.stuck_count = 0
        self.stuck_threshold = 175000
        self.duration = 0
        self.initial_state = None
        self.final_state = None
        self.filepath = self.make_file("simulatedannealing")
        self.best_value = float('-inf')
        self.best_state = None
        self.cache = {}
    
    def accept_probability(self, current_value, neighbor_value, temperature):
        if neighbor_value >= current_value:
            return 1.0
        delta_E = neighbor_value - current_value
        if temperature > self.initial_temp * 0.8:
            prob = math.exp(delta_E / (temperature * 0.01))
        elif temperature > self.initial_temp * 0.4:
            prob = math.exp(delta_E / (temperature * 0.05))
        else:
            prob = math.exp(delta_E / temperature)
        self.exp_deltaE_T.append(prob)
        return prob

    def get_neighbors(self, current: MagicCube, num_neighbors: int = 10) -> List[MagicCube]:
        with ThreadPoolExecutor(max_workers=4) as executor:
            neighbors = list(executor.map(lambda _: current.get_successor("random"), range(num_neighbors)))
        return neighbors

    def update_temperature(self, temperature: float, best_value: float, plateau_count: int) -> float:
        if plateau_count > 10000:
            return temperature * (self.cooling_rate ** 2)
        elif best_value > 80:
            return temperature * (self.cooling_rate ** 0.1)
        elif best_value > 60:
            return temperature * (self.cooling_rate ** 0.25)
        elif best_value > 40:
            return temperature * (self.cooling_rate ** 0.5)
        return temperature * self.cooling_rate

    def reheat_strategy(self, best_value: float) -> float:
        if best_value < 40:
            return self.initial_temp * 0.95
        elif best_value < 60:
            return self.initial_temp * 0.8
        elif best_value < 80:
            return self.initial_temp * 0.6
        return self.initial_temp * 0.4

    def run(self, magic_cube):
        start_time = time.time()
        current = MagicCube(magic_cube.cube)
        self.initial_state = current.cube
        best = MagicCube(current.cube)
        
        temperature = self.initial_temp
        iterations_without_improvement = 0
        total_iterations = 0
        plateau_count = 0
        
        while temperature > self.min_temp and total_iterations < self.max_iterations:
            for _ in range(300):
                if total_iterations >= self.max_iterations:
                    break
                
                neighbors = self.get_neighbors(current, 10)
                best_neighbor = max(neighbors, key=lambda x: x.value)
                
                if self.accept_probability(current.value, best_neighbor.value, temperature) > random.random():
                    current = best_neighbor
                    
                    if current.value > best.value:
                        best = MagicCube(current.cube)
                        iterations_without_improvement = 0
                        plateau_count = 0
                    elif current.value == best.value:
                        plateau_count += 1
                    else:
                        iterations_without_improvement += 1
                else:
                    iterations_without_improvement += 1
                
                self.objective_values.append(current.value)
                self.temperatures.append(temperature)
                total_iterations += 1
                current.save_state(self.filepath)
            
            if iterations_without_improvement >= self.stuck_threshold:
                self.stuck_count += 1
                temperature = self.reheat_strategy(best.value)
                iterations_without_improvement = 0
                plateau_count = 0
                current = MagicCube(best.cube)
                modifications = max(2, min(8, int(80 - best.value)))
                for _ in range(modifications):
                    current = current.get_successor("random")
            else:
                temperature = self.update_temperature(temperature, best.value, plateau_count)

        self.final_state = best.cube
        self.duration = time.time() - start_time
        self.visualize_results()
        return best

    def visualize_results(self):
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 2, 1)
        plt.plot(self.objective_values, 'b-', alpha=0.6)
        plt.title('Objective Function Value vs Iterations')
        plt.xlabel('Iteration')
        plt.ylabel('Value')
        plt.grid(True)
        
        window = 1000
        if len(self.objective_values) > window:
            moving_avg = np.convolve(self.objective_values, np.ones(window)/window, mode='valid')
            plt.plot(range(window-1, len(self.objective_values)), moving_avg, 'r-', linewidth=2)
            plt.legend(['Raw Values', f'Moving Average (window={window})'])
        
        plt.subplot(2, 2, 2)
        plt.plot(self.temperatures)
        plt.title('Temperature vs Iterations')
        plt.xlabel('Iteration')
        plt.ylabel('Temperature')
        plt.grid(True)
        plt.yscale('log')
        
        plt.subplot(2, 2, 3)
        plt.plot(self.exp_deltaE_T)
        plt.title('Acceptance Probability vs Iterations')
        plt.xlabel('Iteration')
        plt.ylabel('e^(ΔE/T)')
        plt.grid(True)
        
        plt.subplot(2, 2, 4)
        plt.axis('off')
        info_text = (
            f"Execution Summary\n\n"
            f"Initial Value: {self.objective_values[0]}\n"
            f"Final Value: {self.objective_values[-1]}\n"
            f"Improvement: {self.objective_values[-1] - self.objective_values[0]}\n"
            f"Times Stuck: {self.stuck_count}\n"
            f"Duration: {self.duration:.2f} seconds"
        )
        plt.text(0.1, 0.5, info_text, fontsize=12)
        
        plt.tight_layout()
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

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sa = SimulatedAnnealing(
        initial_temp=1000000.0,
        cooling_rate=0.99995,
        min_temp=0.0001,
        max_iterations=500000
    )
    initial_cube = MagicCube()
    best_solution = sa.run(initial_cube)