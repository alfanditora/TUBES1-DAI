import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from MagicCube import MagicCube

class SimulatedAnnealing:
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
            # Get neighbor
            neighbor = current.get_successor("random")
            
            # Accept or reject
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
            
            # Check if stuck
            if iterations_without_improvement >= self.stuck_threshold:
                self.stuck_count += 1
                temperature = self.initial_temp * 0.8
                iterations_without_improvement = 0
                current = MagicCube(best.cube)
            
            # Track progress
            self.objective_values.append(current.value)
            self.temperatures.append(temperature)
            
            # Cool down
            temperature *= self.cooling_rate
            total_iterations += 1
        
        self.final_state = best.cube
        self.duration = time.time() - start_time
        
        return best

def visualize_experiment(result):
    plt.figure(figsize=(15, 10))
    
    # Plot objective function
    plt.subplot(2, 2, 1)
    plt.plot(result['objective_values'], 'b-', alpha=0.6)
    plt.title('Objective Function Value vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.grid(True)
    
    # Add moving average
    window = 1000
    if len(result['objective_values']) > window:
        moving_avg = np.convolve(result['objective_values'], 
                               np.ones(window)/window, 
                               mode='valid')
        plt.plot(range(window-1, len(result['objective_values'])), 
                moving_avg, 'r-', linewidth=2, 
                label=f'Moving Average (window={window})')
        plt.legend()
    
    # Plot temperature
    plt.subplot(2, 2, 2)
    plt.plot(result['temperatures'])
    plt.title('Temperature vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Temperature')
    plt.grid(True)
    plt.yscale('log')
    
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

def run_experiments(n_experiments=3):
    all_results = []
    
    for exp in range(n_experiments):
        print(f"\nRunning experiment {exp+1}/{n_experiments}")
        
        # Initialize
        magic_cube = MagicCube()
        sa = SimulatedAnnealing()
        
        # Run algorithm
        best_solution = sa.run(magic_cube)
        
        # Store results
        result = {
            'initial_state': sa.initial_state,
            'final_state': sa.final_state,
            'initial_value': magic_cube.value,
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
    print("\nExperiments Summary:")
    final_values = [r['final_value'] for r in all_results]
    durations = [r['duration'] for r in all_results]
    stuck_counts = [r['stuck_count'] for r in all_results]
    
    print(f"Average Final Value: {np.mean(final_values):.2f}")
    print(f"Best Value Found: {max(final_values)}")
    print(f"Average Duration: {np.mean(durations):.2f}s")
    print(f"Average Times Stuck: {np.mean(stuck_counts):.2f}")

if __name__ == "__main__":
    print("Starting Simulated Annealing experiments...")
    run_experiments(3)