from steepest_ascent import steepest_ascent
from sideways_move import sideways_move
from stochastic import stochastic
from random_restart import random_restart_hill_climbing
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import GeneticAlgorithm
from MagicCube import MagicCube
from visualizer import Visualizer
import os
from typing import Optional
import sys

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def run_experiment(method: int) -> Optional[str]:
    try:
        if method == 1:
            print("\nRunning Steepest Ascent Hill Climbing...")
            S = steepest_ascent()
            S.run()
            return "steepest_ascent.txt"
        elif method == 2:
            print("\nRunning Sideways Move Hill Climbing...")
            SW = sideways_move()
            SW.run()
            return "sideways_move.txt"
        elif method == 3:
            print("\nRunning Stochastic Hill Climbing...")
            SH = stochastic()
            SH.run()
            return "stochastic.txt"
        elif method == 4:
            print("\nRunning Random Restart Hill Climbing...")
            RR = random_restart_hill_climbing()
            RR.run()
            return "random_restart.txt"
        elif method == 5:
            print("\nRunning Simulated Annealing...")
            SA = SimulatedAnnealing()
            initial_cube = MagicCube()
            SA.run_experiments(1)
            return "simulated_annealing.txt"
        elif method == 6:
            print("\nRunning Genetic Algorithm...")
            population_size = int(input("Enter population size (default 500): ") or "500")
            iterations = int(input("Enter number of iterations (default 100): ") or "100")
            GA = GeneticAlgorithm(population_size=population_size, iterations=iterations)
            initial_cube = MagicCube()
            best_cube, best_fitness = GA.run(initial_cube)
            print(f"\nBest fitness achieved: {best_fitness}/109")
            return None  # GA doesn't generate visualization file
        else:
            print("\nInvalid method number!")
            return None
    except Exception as e:
        print(f"\nError running experiment: {str(e)}")
        return None

def list_save_files() -> list:
    directory = "./save_file"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return sorted([f for f in os.listdir(directory) if f.endswith(".txt")])

def main():
    while True:
        clear_screen()
        print("\n=== Magic Cube Local Search Visualization ===\n")
        print("1. Start Experiment")
        print("2. Visualize Results")
        print("3. Help")
        print("4. Exit")
        print()

        try:
            choice = int(input("Enter your choice (1-4): "))

            if choice == 1:
                clear_screen()
                print("\nAvailable Methods:")
                print("1. Steepest Ascent Hill Climbing")
                print("2. Sideways Move Hill Climbing")
                print("3. Stochastic Hill Climbing")
                print("4. Random Restart Hill Climbing")
                print("5. Simulated Annealing")
                print("6. Genetic Algorithm")
                print("0. Back to menu")
                print()

                method = int(input("Choose method (1-6): "))

                if (method != 0):
                    result_file = run_experiment(method)
                    if result_file:
                        print(f"\nExperiment completed! Results saved to: {result_file}")
                    input("\nPress Enter to continue...")

            elif choice == 2:
                clear_screen()

                V = Visualizer()
                V.visualize()

            elif choice == 3:
                clear_screen()
                print("\n=== Help ===")
                print("\n1. Experiment:")
                print("   - Choose a local search method to solve the Magic Cube")
                print("   - Each method will generate a save file (except GA)")
                print("   - Results will be saved in the 'save_file' directory")
                print("\n2. Visualize:")
                print("   - View the step-by-step progress of your experiments")
                print("   - Requires running an experiment first")
                print("   - Not available for Genetic Algorithm")
                print("\n3. Tips:")
                print("   - Try different methods to compare results")
                print("   - For GA, adjust population size and iterations")
                print("   - Use visualization to understand the search process")
                input("\nPress Enter to continue...")

            elif choice == 4:
                print("\nThank you for using Magic Cube Solver!")
                sys.exit(0)

            else:
                print("\nInvalid choice! Please enter a number between 1 and 4.")
                input("\nPress Enter to continue...")

        except ValueError:
            print("\nPlease enter a valid number!")
            input("\nPress Enter to continue...")
        except KeyboardInterrupt:
            print("\n\nExiting program...")
            sys.exit(0)

if __name__ == "__main__":
    main()