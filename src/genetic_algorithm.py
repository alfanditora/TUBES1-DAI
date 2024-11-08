import numpy as np
import time
import matplotlib.pyplot as plt
from typing import List, Tuple
from itertools import combinations
from MagicCube import MagicCube

class GeneticAlgorithmCube:
    def __init__(self, population_size=1000, base_mutation_probability=0.07, iterations=1000):
        self.name = 'Genetic Algorithm for Magic Cube'
        self.iterations = iterations
        self.population_size = population_size
        self.base_mutation_probability = base_mutation_probability
        self.current_mutation_rate = base_mutation_probability
        self.max_mutation_rate = 0.4
        self.stagnation_threshold = 30
        self.mutation_increase_rate = 0.05
        self.avg_fitness_history = []
        self.best_fitness_history = []

    def run(self, init_state):
        start_time = time.time()
        
        population: List[MagicCube] = []
        population.append(init_state)
        
        for _ in range(self.population_size - 1):
            new_cube = MagicCube()
            population.append(new_cube)

        best_individual = population[0]
        best_fitness = best_individual.value
        stagnation_counter = 0
        last_best_fitness = best_fitness
        
        for i in range(self.iterations):
            current_fitness = [cube.value for cube in population]
            avg_fitness = np.mean(current_fitness)
            max_fitness = max(current_fitness)
            
            self.avg_fitness_history.append(avg_fitness)
            self.best_fitness_history.append(max_fitness)

            current_best = max(population, key=lambda x: x.value)
            current_best_fitness = current_best.value
            
            if current_best_fitness <= last_best_fitness:
                stagnation_counter += 1
            else:
                stagnation_counter = 0
                last_best_fitness = current_best_fitness

            if stagnation_counter >= self.stagnation_threshold:
                self._increase_mutation_rate()
                stagnation_counter = 0
            
            if current_best_fitness > best_fitness:
                best_individual = current_best
                best_fitness = current_best_fitness
                self._reset_mutation_rate()

            if (i + 1) % 50 == 0:
                print(f"Iterasi {i+1}: Nilai Terbaik: {best_fitness}/109, Rata-rata: {avg_fitness:.2f}")
                print("\nKubus terbaik saat ini:")
                best_individual.print_cube()

            if best_fitness == 109:
                end_time = time.time()
                print(f"\nSolusi ditemukan pada iterasi {i+1}")
                print(f"Durasi proses: {end_time - start_time:.2f} detik")
                self.plot_progress()
                return best_individual, best_fitness, i + 1

            fitness = self._calculate_fitness(population)
            population = self._selection(population, fitness)
            population = self._crossover(population)
            population = self._mutation(population)

        end_time = time.time()
        print(f"Durasi proses: {end_time - start_time:.2f} detik")
        self.plot_progress()
        return best_individual, best_fitness, self.iterations

    def _increase_mutation_rate(self):
        self.current_mutation_rate = min(
            self.max_mutation_rate,
            self.current_mutation_rate + self.mutation_increase_rate
        )

    def _reset_mutation_rate(self):
        self.current_mutation_rate = self.base_mutation_probability

    def plot_progress(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.best_fitness_history, label='Nilai Terbaik')
        plt.plot(self.avg_fitness_history, label='Rata-rata Populasi')
        plt.xlabel('Iterasi')
        plt.ylabel('Nilai Fitness')
        plt.title('Progress Optimasi Magic Cube')
        plt.legend()
        plt.grid(True)
        plt.show()

    def _calculate_fitness(self, population: List[MagicCube]) -> np.ndarray:
        scores = np.array([cube.value for cube in population])
        scaled_scores = np.exp(scores - np.min(scores))
        return scaled_scores / np.sum(scaled_scores)

    def _selection(self, population: List[MagicCube], fitness: np.ndarray) -> List[MagicCube]:
        elite_size = max(2, self.population_size // 5)
        sorted_indices = np.argsort(fitness)[::-1]
        selected = [population[i] for i in sorted_indices[:elite_size]]
        
        while len(selected) < self.population_size:
            tournament_size = 5
            tournament_indices = np.random.choice(len(population), tournament_size)
            tournament = [population[i] for i in tournament_indices]
            winner = max(tournament, key=lambda x: x.value)
            selected.append(winner)
            
        return selected

    def _crossover(self, parents: List[MagicCube]) -> List[MagicCube]:
        children = []
        elite_size = max(2, self.population_size // 10)
        elite_parents = parents[:elite_size]
        children.extend(elite_parents)
        elite_combinations = list(combinations(elite_parents, 2))
        crossover_methods = ['layer', 'block', 'diagonal', 'random']
        
        for parent1, parent2 in elite_combinations:
            method = np.random.choice(crossover_methods)
            
            if method == 'layer':
                child_cube = parent1.copy_cube(parent1.cube)
                num_layers = np.random.randint(1, 6)
                layers = np.random.choice(5, num_layers, replace=False)
                
                for layer in layers:
                    child_cube[layer] = parent2.copy_cube(parent2.cube)[layer]
                    
            elif method == 'block':
                child_cube = parent1.copy_cube(parent1.cube)
                start_x = np.random.randint(0, 3)
                start_y = np.random.randint(0, 3)
                start_z = np.random.randint(0, 3)
                size_x = np.random.randint(1, 4)
                size_y = np.random.randint(1, 4)
                size_z = np.random.randint(1, 4)
                
                for x in range(start_x, min(start_x + size_x, 5)):
                    for y in range(start_y, min(start_y + size_y, 5)):
                        for z in range(start_z, min(start_z + size_z, 5)):
                            child_cube[x][y][z] = parent2.cube[x][y][z]
                            
            elif method == 'diagonal':
                child_cube = parent1.copy_cube(parent1.cube)
                for i in range(5):
                    child_cube[i][i][i] = parent2.cube[i][i][i]
                    
            else:
                child_cube = parent1.copy_cube(parent1.cube)
                for x in range(5):
                    for y in range(5):
                        for z in range(5):
                            if np.random.random() < 0.3:
                                child_cube[x][y][z] = parent2.cube[x][y][z]
            
            children.append(MagicCube(child_cube))
        
        while len(children) < self.population_size:
            parent1, parent2 = np.random.choice(elite_parents, 2, replace=False)
            method = np.random.choice(crossover_methods)
            
            if method == 'layer':
                child_cube = parent1.copy_cube(parent1.cube)
                num_layers = np.random.randint(1, 6)
                layers = np.random.choice(5, num_layers, replace=False)
                
                for layer in layers:
                    child_cube[layer] = parent2.copy_cube(parent2.cube)[layer]
                    
            elif method == 'block':
                child_cube = parent1.copy_cube(parent1.cube)
                start_x = np.random.randint(0, 3)
                start_y = np.random.randint(0, 3)
                start_z = np.random.randint(0, 3)
                size_x = np.random.randint(1, 4)
                size_y = np.random.randint(1, 4)
                size_z = np.random.randint(1, 4)
                
                for x in range(start_x, min(start_x + size_x, 5)):
                    for y in range(start_y, min(start_y + size_y, 5)):
                        for z in range(start_z, min(start_z + size_z, 5)):
                            child_cube[x][y][z] = parent2.cube[x][y][z]
                            
            elif method == 'diagonal':
                child_cube = parent1.copy_cube(parent1.cube)
                for i in range(5):
                    child_cube[i][i][i] = parent2.cube[i][i][i]
                    
            else:
                child_cube = parent1.copy_cube(parent1.cube)
                for x in range(5):
                    for y in range(5):
                        for z in range(5):
                            if np.random.random() < 0.3:
                                child_cube[x][y][z] = parent2.cube[x][y][z]
                                
            children.append(MagicCube(child_cube))
        
        children.sort(key=lambda x: x.calculate_value(), reverse=True)
        return children[:self.population_size]    
    
    def _mutation(self, population: List[MagicCube]) -> List[MagicCube]:
        mutated = []
        for individual in population:
            if np.random.random() < self.current_mutation_rate:
                mutated_cube = individual
                n_swaps = np.random.randint(1, max(8, int(15 * self.current_mutation_rate)))
                
                for _ in range(n_swaps):
                    pos1 = (np.random.randint(0, 5), np.random.randint(0, 5), np.random.randint(0, 5))
                    pos2 = (np.random.randint(0, 5), np.random.randint(0, 5), np.random.randint(0, 5))
                    while pos1 == pos2:
                        pos2 = (np.random.randint(0, 5), np.random.randint(0, 5), np.random.randint(0, 5))
                    
                    new_cube = mutated_cube.swap_positions(mutated_cube.cube, pos1, pos2)
                    mutated_cube = MagicCube(new_cube)
                
                mutated.append(mutated_cube)
            else:
                mutated.append(individual)
        return mutated
    
def main():
    population_size = 300
    max_iterations = 1000
    
    ga = GeneticAlgorithmCube(
        population_size=population_size,
        iterations=max_iterations
    )
    
    initial_state = MagicCube()
    
    print("=== Genetic Algorithm untuk Magic Cube ===")
    print(f"Populasi: {population_size}")
    print(f"Maksimum Iterasi: {max_iterations}")
    print("\nState awal:")
    initial_state.print_cube()
    print(f"Nilai awal: {initial_state.value}/109")
    
    print("\nMemulai optimasi...\n")
    best_cube, best_fitness, iterations = ga.run(initial_state)
    
    print("\n=== Hasil Optimasi ===")
    print(f"Iterasi yang dilakukan: {iterations}")
    print(f"Nilai akhir: {best_fitness}/109")
    print("\nKubus hasil optimasi:")
    best_cube.print_cube()

if __name__ == "__main__":
    main()