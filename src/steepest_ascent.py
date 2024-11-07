from MagicCube import MagicCube
import matplotlib.pyplot as plt

class steepest_ascent(object):
    def __init__(self):
        self.list_of_value = []

    def run(self):
        current = MagicCube()
        self.list_of_value.append(current.value)
        current.print_cube()
        i = 0

        while True:
            successor = current.get_successor("best")
            if current.value == 109:
                break
            if successor.value <= current.value:
                break
            else:
                self.list_of_value.append(current.value)
                current = successor
                
            i += 1

        current.print_cube()
        print(i)
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
    H = steepest_ascent()
    H.run()