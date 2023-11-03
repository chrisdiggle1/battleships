import random


class Board:
    def __init__(self, size=6, num_ships=5):
        """
        Initializes the game board with a specific size and places ships 
        at random locations.
        """
        self.size = size
        self.num_ships = num_ships
        self.grid = [["." for _ in range(size)] for _ in range(size)]

    def initialise_board(self):
        """
        Initialize the game board with water represented by dots and creates
        a 6x6 game grid.
        """
        return [["." for _ in range(self.size)] for _ in range(self.size)]

    def print_board(self):
        """
        Print the game board in a format the user can read.
        """
        print("   " + " ".join(str(i + 1) for i in range(self.size)))
        for r in range(self.size):
            print(str(r + 1) + "  " + " ".join(self.grid[r]))


player_board = Board()
computer_board = Board()

print("Your board:")
player_board.print_board()
print("\nComputer's board (with ships hidden):")
computer_board.print_board()
