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
        self.objective_values = []
        self.temperatures = []
        self.exp_deltaE_T = []
        self.stuck_count = 0
        self.stuck_threshold = 175000  
        self.duration = 0
        self.initial_state = None
        self.final_state = None
    
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
                    
                best_neighbor = None
                best_neighbor_value = float('-inf')
                
                for _ in range(10):  
                    neighbor = current.get_successor("random")
                    if neighbor.value > best_neighbor_value:
                        best_neighbor = neighbor
                        best_neighbor_value = neighbor.value
                
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
            
            if iterations_without_improvement >= self.stuck_threshold:
                self.stuck_count += 1
                if best.value < 40:
                    temperature = self.initial_temp * 0.95  
                elif best.value < 60:
                    temperature = self.initial_temp * 0.8  
                elif best.value < 80:
                    temperature = self.initial_temp * 0.6  
                else:
                    temperature = self.initial_temp * 0.4  
                
                iterations_without_improvement = 0
                plateau_count = 0
                current = MagicCube(best.cube)
                modifications = max(2, min(8, int(80 - best.value)))  
                for _ in range(modifications):
                    current = current.get_successor("random")
            else:
                if plateau_count > 10000:  
                    temperature *= (self.cooling_rate ** 2)     
                elif best.value > 80:
                    temperature *= (self.cooling_rate ** 0.1)    
                elif best.value > 60:
                    temperature *= (self.cooling_rate ** 0.25)  
                elif best.value > 40:
                    temperature *= (self.cooling_rate ** 0.5)    
                else:
                    temperature *= self.cooling_rate             
        self.final_state = best.cube
        self.duration = time.time() - start_time
        return best

def run_experiments(n_experiments=3):
    all_results = []
    for exp in range(n_experiments):
        print(f"\nRunning experiment {exp+1}/{n_experiments}")
        
        sa = SimulatedAnnealing(
            initial_temp=1000000.0,
            cooling_rate=0.99995,
            min_temp=0.0001,
            max_iterations=1000
        )
        magic_cube = MagicCube()
        initial_value = magic_cube.value
        best_solution = sa.run(magic_cube)
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
        visualize_experiment(result)
    
    visualize_summary(all_results)
    return all_results

def visualize_experiment(result):
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 2, 1)
    plt.plot(result['objective_values'], 'b-', alpha=0.6)
    plt.title('Objective Function Value vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Value')
    plt.grid(True)
    
    window = 1000
    if len(result['objective_values']) > window:
        moving_avg = np.convolve(result['objective_values'], 
                               np.ones(window)/window, 
                               mode='valid')
        plt.plot(range(window-1, len(result['objective_values'])), 
                moving_avg, 'r-', linewidth=2, 
                label=f'Moving Average (window={window})')
        plt.legend()
    
    plt.subplot(2, 2, 2)
    plt.plot(result['temperatures'])
    plt.title('Temperature vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Temperature')
    plt.grid(True)
    plt.yscale('log')
    plt.subplot(2, 2, 3)
    plt.plot(result['exp_deltaE_T'])
    plt.title('e^(ΔE/T) vs Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('e^(ΔE/T)')
    plt.grid(True)
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
    print("\nInitial State:")
    MagicCube(result['initial_state']).print_cube()
    print("\nFinal State:")
    MagicCube(result['final_state']).print_cube()

def visualize_summary(results):
    plt.figure(figsize=(15, 10))
    plt.subplot(2, 2, 1)
    final_values = [r['final_value'] for r in results]
    plt.bar(range(1, len(results) + 1), final_values, color='skyblue')
    plt.title('Final Values Across Experiments')
    plt.xlabel('Experiment')
    plt.ylabel('Value')
    plt.grid(True)
    
    for i, v in enumerate(final_values):
        plt.text(i + 1, v, str(v), ha='center', va='bottom')
    
    plt.subplot(2, 2, 2)
    durations = [r['duration'] for r in results]
    plt.bar(range(1, len(results) + 1), durations, color='lightgreen')
    plt.title('Duration of Experiments')
    plt.xlabel('Experiment')
    plt.ylabel('Seconds')
    plt.grid(True)
    
    plt.subplot(2, 2, 3)
    stuck_counts = [r['stuck_count'] for r in results]
    plt.bar(range(1, len(results) + 1), stuck_counts, color='salmon')
    plt.title('Times Stuck in Local Optima')
    plt.xlabel('Experiment')
    plt.ylabel('Count')
    plt.grid(True)
    
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
    results = run_experiments(3)