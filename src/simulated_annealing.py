import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from MagicCube import MagicCube

class SimulatedAnnealing:
    def __init__(self, initial_temp=10000.0, cooling_rate=0.999, min_temp=0.1, max_iterations=100000):
        self.initial_temp = initial_temp
        self.cooling_rate = cooling_rate
        self.min_temp = min_temp
        self.max_iterations = max_iterations
        
        # Tracking metrics
        self.objective_values = []
        self.temperatures = []
        self.exp_deltaE_T = []
        self.stuck_count = 0
        self.stuck_threshold = 10000
        self.duration = 0
        
        # States
        self.initial_state = None
        self.final_state = None
    
    def accept_probability(self, current_value, neighbor_value, temperature):
        if neighbor_value >= current_value:
            return 1.0
        
        delta_E = neighbor_value - current_value
        prob = math.exp(delta_E / temperature)
        self.exp_deltaE_T.append(prob)
        return prob
    
    def run(self, magic_cube):
        start_time = time.time()
        
        # Save initial state
        current = MagicCube(magic_cube.cube)
        self.initial_state = current.cube
        best = MagicCube(current.cube)
        
        temperature = self.initial_temp
        iterations_without_improvement = 0
        total_iterations = 0
        
        while temperature > self.min_temp and total_iterations < self.max_iterations:
            # Multiple attempts at each temperature level
            for _ in range(50):
                if total_iterations >= self.max_iterations:
                    break
                    
                # Get random neighbor
                neighbor = current.get_successor("random")
                
                # Calculate acceptance probability
                if self.accept_probability(current.value, neighbor.value, temperature) > random.random():
                    current = neighbor
                    
                    # Update best if improved
                    if current.value > best.value:
                        best = MagicCube(current.cube)
                        iterations_without_improvement = 0
                    else:
                        iterations_without_improvement += 1
                else:
                    iterations_without_improvement += 1
                
                # Track progress
                self.objective_values.append(current.value)
                self.temperatures.append(temperature)
                
                total_iterations += 1
            
            # Check if stuck
            if iterations_without_improvement >= self.stuck_threshold:
                self.stuck_count += 1
                # Reheat when stuck
                temperature = self.initial_temp * 0.5
                iterations_without_improvement = 0
            else:
                # Normal cooling
                temperature *= self.cooling_rate
        
        self.final_state = best.cube
        self.duration = time.time() - start_time
        
        return best

def run_experiments(n_experiments=3):
    all_results = []
    
    for exp in range(n_experiments):
        print(f"\nRunning experiment {exp+1}/{n_experiments}")
        
        # Initialize with optimized parameters
        sa = SimulatedAnnealing(
            initial_temp=10000.0,
            cooling_rate=0.999,
            min_temp=0.1,
            max_iterations=100000
        )
        
        magic_cube = MagicCube()
        initial_value = magic_cube.value
        
        # Run algorithm
        best_solution = sa.run(magic_cube)
        
        # Store results
        result = {
            'experiment': exp + 1,
            'initial_state': sa.initial_state,
            'final_state': sa.final_state,
            'initial_value': initial_value,
            'final_value': best_solution.value,
            'objective_values': sa.objective_values,
            'temperatures': sa.temperatures,
            'exp_deltaE_T': sa.exp_deltaE_T,
            'stuck_count': sa.stuck_count,
            'duration': sa.duration
        }
        all_results.append(result)
        
        # Visualize individual experiment
        visualize_experiment(result)
    
    # Visualize summary
    visualize_summary(all_results)
    return all_results

def visualize_experiment(result):
    """Visualize results for a single experiment"""
    plt.figure(figsize=(15, 10))
    
    # Plot objective function
    plt.subplot(2, 2, 1)
    plt.plot(result['objective_values'])
    plt.title('Objective Function Value vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.grid(True)
    
    # Plot temperature
    plt.subplot(2, 2, 2)
    plt.plot(result['temperatures'])
    plt.title('Temperature vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Temperature')
    plt.grid(True)
    
    # Plot e^(ΔE/T)
    plt.subplot(2, 2, 3)
    plt.plot(result['exp_deltaE_T'])
    plt.title('e^(ΔE/T) vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('e^(ΔE/T)')
    plt.grid(True)
    
    # Display experiment info
    plt.subplot(2, 2, 4)
    plt.axis('off')
    info_text = (
        f"Experiment {result['experiment']}\n\n"
        f"Initial Value: {result['initial_value']}\n"
        f"Final Value: {result['final_value']}\n"
        f"Improvement: {result['final_value'] - result['initial_value']}\n"
        f"Times Stuck: {result['stuck_count']}\n"
        f"Duration: {result['duration']:.2f} seconds"
    )
    plt.text(0.1, 0.5, info_text, fontsize=12)
    
    plt.tight_layout()
    plt.show()
    
    # Print cube states
    print("\nInitial State:")
    MagicCube(result['initial_state']).print_cube()
    print("\nFinal State:")
    MagicCube(result['final_state']).print_cube()

def visualize_summary(results):
    """Visualize summary of all experiments"""
    plt.figure(figsize=(15, 10))
    
    # Plot final values
    plt.subplot(2, 2, 1)
    final_values = [r['final_value'] for r in results]
    plt.bar(range(1, len(results) + 1), final_values)
    plt.title('Final Values Across Experiments')
    plt.xlabel('Experiment')
    plt.ylabel('Value')
    plt.grid(True)
    
    # Plot durations
    plt.subplot(2, 2, 2)
    durations = [r['duration'] for r in results]
    plt.bar(range(1, len(results) + 1), durations)
    plt.title('Duration of Experiments')
    plt.xlabel('Experiment')
    plt.ylabel('Seconds')
    plt.grid(True)
    
    # Plot stuck counts
    plt.subplot(2, 2, 3)
    stuck_counts = [r['stuck_count'] for r in results]
    plt.bar(range(1, len(results) + 1), stuck_counts)
    plt.title('Times Stuck in Local Optima')
    plt.xlabel('Experiment')
    plt.ylabel('Count')
    plt.grid(True)
    
    # Display summary statistics
    plt.subplot(2, 2, 4)
    plt.axis('off')
    summary_text = (
        f"Summary Statistics\n\n"
        f"Average Final Value: {np.mean(final_values):.2f}\n"
        f"Best Value Found: {max(final_values)}\n"
        f"Average Duration: {np.mean(durations):.2f}s\n"
        f"Average Times Stuck: {np.mean(stuck_counts):.2f}\n"
        f"Total Experiments: {len(results)}"
    )
    plt.text(0.1, 0.5, summary_text, fontsize=12)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Run experiments
    results = run_experiments(3)