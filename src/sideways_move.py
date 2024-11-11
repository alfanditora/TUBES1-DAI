from MagicCube import MagicCube
import matplotlib.pyplot as plt
import time
import os

class sideways_move(object):
    def __init__(self, max_sideways_moves = 100):
        self.list_of_value = []
        self.max_sideways_moves = max_sideways_moves
        self.iteration = 0
        self.duration = 0
        self.total_sideways = 0
        self.filepath = self.make_file("sidewaysmove")
    
    def run(self):
        start_time = time.time()

        current = MagicCube()
        self.list_of_value.append(current.value)
        current.print_cube()
        i = 0
        sideways_moves = 0

        while True and sideways_moves < self.max_sideways_moves:
            successor = current.get_successor("best")
    
            if successor.value == current.value:
                sideways_moves += 1
            elif successor.value < current.value:
                break
            else:
                sideways_moves = 0
                
            current = successor
            self.list_of_value.append(current.value)
            current.save_state(self.filepath)
            i += 1

        current.print_cube()
        self.duration = time.time() - start_time
        self.iteration = i
        self.total_sideways = sideways_moves
        print(self.duration)
        print(self.iteration)
        print(f"Total sideways moves: {sideways_moves}")
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
            f"Total sideways: {self.total_sideways}\n"
            f"Duration: {self.duration:.2f} seconds"
        )
        plt.text(0.1, 0.5, info_text, fontsize=12, verticalalignment='center')
        
        plt.tight_layout()
        plt.show()

    def make_file(self, name):
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

if __name__ == "__main__":
    S = sideways_move()
    S.run()