import random
import math
import time
import matplotlib.pyplot as plt
import numpy as np
from MagicCube import MagicCube

class SimulatedAnnealing:
    def __init__(self):
        # Parameter standar
        self.initial_temp = 1000000.0
        self.cooling_rate = 0.99995
        self.min_temp = 0.0001
        self.max_iter = 500000
        
        # Tracking
        self.values = []  # objective function values
        self.temps = []   # temperature history
        self.probs = []   # acceptance probabilities
        self.stuck = 0    # stuck counter
        self.duration = 0
        self.thresh = 175000  # stuck threshold
        
        # States
        self.start_state = None
        self.end_state = None

    def get_probability(self, old_val, new_val, temp):
        if new_val >= old_val:
            return 1.0
        delta = new_val - old_val
        prob = math.exp(delta / temp)
        self.probs.append(prob)
        return prob

    def optimize(self, magic_cube):
        start = time.time()
        
        # Setup
        current = MagicCube(magic_cube.cube)
        self.start_state = current.cube
        best = MagicCube(current.cube)
        
        temp = self.initial_temp
        no_improve = 0
        iters = 0
        
        # Main loop
        while temp > self.min_temp and iters < self.max_iter:
            neighbor = current.get_successor("random")
            
            # Accept/reject neighbor
            if self.get_probability(current.value, neighbor.value, temp) > random.random():
                current = neighbor
                if current.value > best.value:
                    best = MagicCube(current.cube)
                    no_improve = 0
                else:
                    no_improve += 1
            else:
                no_improve += 1
            
            # Handle stuck case
            if no_improve >= self.thresh:
                self.stuck += 1
                temp = self.initial_temp * 0.8
                no_improve = 0
                current = MagicCube(best.cube)
            
            # Track progress
            self.values.append(current.value)
            self.temps.append(temp)
            
            # Cool system
            temp *= self.cooling_rate
            iters += 1
        
        self.end_state = best.cube
        self.duration = time.time() - start
        return best

def show_experiment(data):
    plt.figure(figsize=(12, 8))
    
    # Values plot
    plt.subplot(2, 2, 1)
    plt.plot(data['values'])
    plt.title('Values over Time')
    plt.grid(True)
    
    # Temperature plot
    plt.subplot(2, 2, 2)
    plt.plot(data['temps'])
    plt.title('Temperature Change')
    plt.yscale('log')
    plt.grid(True)
    
    # Probabilities plot
    plt.subplot(2, 2, 3)
    plt.plot(data['probs'])
    plt.title('Acceptance Probabilities')
    plt.grid(True)
    
    # Info box
    plt.subplot(2, 2, 4)
    plt.axis('off')
    info = (
        f"Start Value: {data['start_val']}\n"
        f"End Value: {data['end_val']}\n"
        f"Change: {data['end_val'] - data['start_val']}\n"
        f"Stuck Times: {data['stuck']}\n"
        f"Time: {data['time']:.2f}s"
    )
    plt.text(0.1, 0.5, info, fontsize=10)
    
    plt.tight_layout()
    plt.show()

def run_tests(count=3):
    results = []
    
    for i in range(count):
        print(f"\nTest {i+1}/{count}")
        
        cube = MagicCube()
        sa = SimulatedAnnealing()
        best = sa.optimize(cube)
        
        # Collect data
        data = {
            'start_val': cube.value,
            'end_val': best.value,
            'values': sa.values,
            'temps': sa.temps,
            'probs': sa.probs,
            'stuck': sa.stuck,
            'time': sa.duration
        }
        results.append(data)
        
        # Show results
        show_experiment(data)
        
        # Show cube states
        print("\nStarting State:")
        MagicCube(sa.start_state).print_cube()
        print("\nFinal State:")
        MagicCube(sa.end_state).print_cube()
    
    # Show summary
    print("\nOverall Results:")
    end_vals = [r['end_val'] for r in results]
    times = [r['time'] for r in results]
    print(f"Average Value: {np.mean(end_vals):.2f}")
    print(f"Best Value: {max(end_vals)}")
    print(f"Average Time: {np.mean(times):.2f}s")

if __name__ == "__main__":
    print("Running Simulated Annealing Tests...")
    run_tests(3)