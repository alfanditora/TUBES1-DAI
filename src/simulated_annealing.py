import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from MagicCube import MagicCube

class ModifiedSimulatedAnnealing:
    def __init__(self, initial_temp=1000000.0, cooling_rate=0.99995, min_temp=0.0001, max_iterations=500000):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iterations = max_iterations
        
        # Tracking metrics
        self.objective_values = []
        self.temperatures = []
        self.exp_deltaE_T = []
        self.stuck_count = 0
        self.stuck_threshold = 175000
        self.duration = 0
        
        # Additional tracking
        self.best_values = []
        self.improvement_rates = []
        self.phase_changes = []
        
        # States
        self.initial_state = None
        self.final_state = None
    
    def get_neighbors(self, current, num_neighbors=10):
        neighbors = []
        for _ in range(num_neighbors):
            if random.random() < 0.7:  # 70% chance of regular swap
                neighbor = current.get_successor("random")
            else:  # 30% chance of multiple swaps
                neighbor = current
                for _ in range(3):
                    neighbor = neighbor.get_successor("random")
            neighbors.append(neighbor)
        return neighbors
    
    def accept_probability(self, current_value, neighbor_value, temperature, progress):
        if neighbor_value >= current_value:
            return 1.0
        
        delta_E = neighbor_value - current_value
        
        # Adaptive acceptance based on search progress
        if progress < 0.3:  # Early stage - more exploratory
            prob = math.exp(delta_E / (temperature * 0.08))
        elif progress < 0.7:  # Mid stage - balanced
            if current_value < 30:
                prob = math.exp(delta_E / (temperature * 0.05))
            else:
                prob = math.exp(delta_E / temperature)
        else:  # Late stage - more selective
            prob = math.exp(delta_E / (temperature * 1.2))
        
        self.exp_deltaE_T.append(prob)
        return prob
    
    def adaptive_reheat(self, best_value, temperature):
        if best_value < 25:
            return self.initial_temp * 0.95  # Strong reheat
        elif best_value < 35:
            return self.initial_temp * 0.8   # Moderate reheat
        elif best_value < 45:
            return temperature * 2           # Light reheat
        else:
            return temperature * 1.5         # Very light reheat
    
    def run(self, magic_cube):
        start_time = time.time()
        
        # Initialize
        current = MagicCube(magic_cube.cube)
        self.initial_state = current.cube
        best = MagicCube(current.cube)
        
        temperature = self.initial_temp
        iterations_without_improvement = 0
        total_iterations = 0
        phase = "exploration"
        last_improvement = 0
        
        while temperature > self.min_temp and total_iterations < self.max_iterations:
            progress = total_iterations / self.max_iterations
            
            # Generate and evaluate multiple neighbors
            neighbors = self.get_neighbors(current)
            best_neighbor = max(neighbors, key=lambda x: x.value)
            
            # Calculate acceptance probability
            if self.accept_probability(current.value, best_neighbor.value, 
                                    temperature, progress) > random.random():
                current = best_neighbor
                
                # Update best if improved
                if current.value > best.value:
                    best = MagicCube(current.cube)
                    iterations_without_improvement = 0
                    last_improvement = total_iterations
                    
                    # Track improvement rate
                    self.improvement_rates.append(
                        (total_iterations, current.value - best.value)
                    )
                else:
                    iterations_without_improvement += 1
            else:
                iterations_without_improvement += 1
            
            # Phase detection and adaptation
            if phase == "exploration" and temperature < self.initial_temp * 0.5:
                phase = "intensification"
                self.phase_changes.append(("intensification", total_iterations))
            elif phase == "intensification" and temperature < self.initial_temp * 0.1:
                phase = "convergence"
                self.phase_changes.append(("convergence", total_iterations))
            
            # Check if stuck
            if iterations_without_improvement >= self.stuck_threshold:
                self.stuck_count += 1
                temperature = self.adaptive_reheat(best.value, temperature)
                iterations_without_improvement = 0
                
                # Return to best state with some randomization
                current = MagicCube(best.cube)
                for _ in range(random.randint(2, 5)):
                    current = current.get_successor("random")
            else:
                # Adaptive cooling based on phase and performance
                if phase == "exploration":
                    temperature *= self.cooling_rate
                elif phase == "intensification":
                    if best.value > 40:
                        temperature *= (self.cooling_rate ** 0.7)
                    else:
                        temperature *= self.cooling_rate
                else:  # convergence
                    temperature *= (self.cooling_rate ** 1.2)
            
            # Track progress
            self.objective_values.append(current.value)
            self.temperatures.append(temperature)
            self.best_values.append(best.value)
            
            total_iterations += 1
        
        self.final_state = best.cube
        self.duration = time.time() - start_time
        
        return best

    def visualize_search_phases(self):
        plt.figure(figsize=(15, 5))
        plt.plot(self.objective_values, 'b-', alpha=0.3, label='Current Value')
        plt.plot(self.best_values, 'r-', label='Best Value')
        
        # Mark phase changes
        for phase, iteration in self.phase_changes:
            plt.axvline(x=iteration, color='g', linestyle='--', alpha=0.5)
            plt.text(iteration, plt.ylim()[1], phase, rotation=90)
            
        plt.title('Search Progress with Phase Changes')
        plt.xlabel('Iteration')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.show()