from MagicCube import MagicCube
import matplotlib.pyplot as plt
import time

class stochastic(object):
    def __init__(self, max_iterations=100000):
        self.max_iterations = max_iterations
        self.list_of_value = []
        self.iteration = 0
        self.duration = 0
    
    def run(self):
        start_time = time.time()

        current = MagicCube()
        self.list_of_value.append(current.value)
        current.print_cube()
        it = 0

        for i in range(self.max_iterations):
            successor = current.get_successor("random")
            if successor.value > current.value:
                current = successor
                
            self.list_of_value.append(current.value)
            it += 1

        current.print_cube()
        self.duration = time.time() - start_time
        self.iteration = i + 1
        print(self.duration)
        print(self.iteration)
        self.makePlot()

    def makePlot(self):
        plt.figure(figsize=(12, 8))
        
        plt.subplot(2, 1, 1)
        plt.plot(list(range(len(self.list_of_value))), self.list_of_value)
        plt.title("Magic Cube Value over Iterations")
        plt.xlabel("Iteration")
        plt.ylabel("Value")
        plt.grid(True)
        
        plt.subplot(2, 1, 2)
        plt.axis('off')
        info_text = (
            f"Initial Value: {self.list_of_value[0]}\n"
            f"Final Value: {self.list_of_value[-1]}\n"
            f"Total Iterations: {self.iteration}\n"
            f"Duration: {self.duration:.2f} seconds"
        )
        plt.text(0.1, 0.5, info_text, fontsize=12, verticalalignment='center')
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    SH = stochastic()
    SH.run()