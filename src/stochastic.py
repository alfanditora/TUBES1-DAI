from MagicCube import MagicCube
import matplotlib.pyplot as plt

class stochastic(object):
    def __init__(self, max_iterations=10000):
        self.max_iterations = max_iterations
        self.list_of_value = []
    
    def run(self):
        current = MagicCube()
        self.list_of_value.append(current.value)
        current.print_cube()
        it = 0

        for i in range(self.max_iterations):
            successor = current.get_successor("random")
            if (current.value == 109):
                break
            if successor.value > current.value:
                current = successor
                self.list_of_value.append(current.value)
                
            it += 1

        current.print_cube()
        print(it)
        self.makePlot()

    def makePlot(self):
        plt.figure(figsize=(12, 6))
        plt.plot(list(range(len(self.list_of_value))), self.list_of_value)
        plt.title("Magic Cube Value over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Value")
        plt.grid()
        plt.show()

if __name__ == "__main__":
    SH = stochastic()
    SH.run()