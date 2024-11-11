from steepest_ascent import steepest_ascent
from sideways_move import sideways_move
from stochastic import stochastic
from random_restart import random_restart_hill_climbing
from simulated_annealing import SimulatedAnnealing
from genetic_algorithm import SimpleGeneticAlgorithm
from MagicCube import MagicCube
from visualizer import Visualizer
import os
menuSTATE = True
x = 0
while menuSTATE:
    print("\n\nMENU\n\n")
    print("1. Start experiment!!")
    print("2. Visualize!!")
    print("3. Help??")
    print("4. Exit:(")
    print()
    x = input("Enter your number: ")
    x = int(x)
    print()
    if x == 1:
        print("Choose your method:\n")
        print("1. Steepest Ascent")
        print("2. Sideways Move")
        print("3. Stochastic")
        print("4. Random restart")
        print("5. Simulated Annealing")
        print("6. Genetic Algorithm")
        print()
        y = int(input("Enter your number: "))
        print()
        print()
        if y == 1:
            S = steepest_ascent()
            S.run()
        elif y == 2:
            SW = sideways_move()
            SW.run()
        elif y == 3:
            SH = stochastic()
            SH.run()
        elif y == 4:
            RR = random_restart_hill_climbing()
            RR.run()
        elif y == 5:
            pass
        elif y == 6:
            GA = SimpleGeneticAlgorithm(population_size=500, iterations=100)
            initial_cube = MagicCube()
            best_cube, best_fitness = GA.run(initial_cube)
        else:
            print("Upss, Wrong number!!\n")
    elif x == 2:
        print("Choose your save file:\n")
        directory = ".\\save_file"
        txt_files = sorted([f for f in os.listdir(directory) if f.endswith(".txt")])

        if txt_files:
            print("Save file:\n")
            for file_name in txt_files:
                print(f"- {file_name}\n")
        else:
            print("File doesnt exist!\n")

        filename = input("Input save file name: ")
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            V = Visualizer()
            V.load_file(filename)
            V.visualize()

    elif x == 3:
        print("HELPPPPP!!!!!\n")
        print("1. Experiment with local search")
        print("2. Visualize your experiment! RUN FIRST! NO GENETIC!!")
        print("3. Showing help!")
        print("4. Exit program:(")
    elif x == 4:
        menuSTATE = False
        break
    else:
        print("Upss, Wrong number!!\n")"