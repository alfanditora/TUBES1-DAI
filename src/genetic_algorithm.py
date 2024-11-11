import numpy as np
import time
import matplotlib.pyplot as plt
from typing import List, Tuple, Optional
from MagicCube import MagicCube
import os
import logging
from dataclasses import dataclass
import random
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

@dataclass
class GeneticConfig:
    population_size: int = 100
    iterations: int = 100
    mutation_rate: float = 0.1
    tournament_size: int = 3
    elite_size: int = 4
    crossover_points: int = 2
    parallel_processing: bool = True
    max_workers: int = 4

class GeneticAlgorithm:
    def __init__(self, population_size=100, iterations=100):
        self.population_size = population_size
        self.mutation_rate = 0.1
        self.iterations = iterations
        self.avg_fitness_history = []
        self.best_fitness_history = []
        self.execution_time = None
        self.initial_fitness = None
        self.final_fitness = None
        self.filepath = self.make_file("geneticalgorithm")
        self.population_cache = {}

    def calculate_fitness(self, population: List[MagicCube]) -> List[float]:
        with ThreadPoolExecutor(max_workers=4) as executor:
            return list(executor.map(lambda cube: cube.value, population))

    def tournament_select(self, population: List[MagicCube], fitness: List[float], tournament_size: int = 3) -> MagicCube:
        tournament_idx = np.random.choice(len(population), tournament_size, replace=False)
        tournament = [(fitness[i], population[i]) for i in tournament_idx]
        return max(tournament, key=lambda x: x[0])[1]

    def selection(self, population: List[MagicCube], fitness: List[float]) -> List[MagicCube]:
        population_with_fitness = list(zip(fitness, population))
        population_with_fitness.sort(key=lambda x: x[0], reverse=True)
        sorted_population = [cube for _, cube in population_with_fitness]
        elite_size = max(2, self.population_size // 4)
        elite = sorted_population[:elite_size]
        
        new_population = elite.copy()
        while len(new_population) < self.population_size:
            parent = self.tournament_select(population, fitness)
            new_population.append(MagicCube(parent.copy_cube(parent.cube)))
        
        return new_population

    def crossover(self, population: List[MagicCube]) -> List[MagicCube]:
        children = []
        elite_size = max(2, self.population_size // 10)
        children.extend(population[:elite_size])
        
        while len(children) < self.population_size:
            parent1, parent2 = np.random.choice(population[:elite_size], 2, replace=False)
            child_cube = parent1.copy_cube(parent1.cube)
            n_layers = np.random.randint(1, 4)
            layers = np.random.choice(5, n_layers, replace=False)
            
            for layer in layers:
                child_cube[layer] = parent2.copy_cube(parent2.cube)[layer]
            children.append(MagicCube(child_cube))
        
        return children

    def mutation(self, population: List[MagicCube]) -> List[MagicCube]:
        mutated = []
        for cube in population:
            if np.random.random() < self.mutation_rate:
                mutated_cube = cube
                n_mutations = np.random.randint(1, 4)
                
                for _ in range(n_mutations):
                    pos1 = (np.random.randint(0, 5), np.random.randint(0, 5), np.random.randint(0, 5))
                    pos2 = (np.random.randint(0, 5), np.random.randint(0, 5), np.random.randint(0, 5))
                    while pos1 == pos2:
                        pos2 = (np.random.randint(0, 5), np.random.randint(0, 5), np.random.randint(0, 5))
                    new_cube = mutated_cube.swap_positions(mutated_cube.cube, pos1, pos2)
                    mutated_cube = MagicCube(new_cube)
                
                mutated.append(mutated_cube)
            else:
                mutated.append(cube)
        return mutated

    def plot_progress(self):
        fig = plt.figure(figsize=(15, 10))
        ax1 = plt.subplot(2, 1, 1)
        ax1.plot(self.best_fitness_history, label='Best Value', color='blue')
        ax1.plot(self.avg_fitness_history, label='Population Average', color='red')
        ax1.set_xlabel('Generation')
        ax1.set_ylabel('Fitness')
        ax1.set_title('Magic Cube Optimization Progress')
        ax1.legend()
        ax1.grid(True)

        info_text = (
            f'Optimization Info:\n'
            f'Population Size: {self.population_size}\n'
            f'Total Generations: {len(self.best_fitness_history)}\n'
            f'Duration: {self.execution_time:.2f} seconds\n'
            f'Initial Value: {self.initial_fitness}/109\n'
            f'Final Value: {self.final_fitness}/109'
        )
        
        plt.figtext(0.15, 0.15, info_text, bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'), 
                   fontsize=10, family='monospace')
        
        ax2 = plt.subplot(2, 1, 2)
        ax2.axis('off')
        plt.tight_layout()
        plt.show()

    def run(self, init_state: MagicCube) -> Tuple[MagicCube, float]:
        start_time = time.time()
        self.initial_fitness = init_state.value
        
        population = [init_state]
        for _ in range(self.population_size - 1):
            population.append(MagicCube())

        best_fitness = init_state.value
        best_cube = init_state
        
        print(f"\nInitial cube (fitness: {best_fitness}/109):")
        init_state.print_cube()
        print("\nStarting optimization...\n")
        
        for generation in range(self.iterations):
            fitness = self.calculate_fitness(population)
            current_best = max(fitness)
            avg_fitness = sum(fitness) / len(fitness)
            
            self.best_fitness_history.append(current_best)
            self.avg_fitness_history.append(avg_fitness)
            
            if current_best > best_fitness:
                best_fitness = current_best
                best_cube = population[fitness.index(current_best)]
                print(f"Generation {generation + 1}: New best fitness = {best_fitness}")
            
            if best_fitness == 109:
                print(f"\nSolution found at generation {generation + 1}")
                break
            
            population = self.selection(population, fitness)
            population = self.crossover(population)
            population = self.mutation(population)
            best_cube.save_state(self.filepath)

        self.execution_time = time.time() - start_time
        self.final_fitness = best_fitness
        
        print(f"\nExecution time: {self.execution_time:.2f} seconds")
        print(f"Final best fitness: {best_fitness}/109")
        print("\nFinal best cube structure:")
        best_cube.print_cube()
        
        self.plot_progress()
        return best_cube, best_fitness

    def make_file(self, name: str) -> str:
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

def main():
    ga = GeneticAlgorithm(
        population_size=500,
        iterations=100
    )
    
    initial_cube = MagicCube()
    best_cube, best_fitness = ga.run(initial_cube)

if __name__ == "__main__":
    main()