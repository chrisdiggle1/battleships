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
        self.place_ships()

    def initialise_board(self):
        """
        Initialize the game board with water represented by dots and creates
        a 6x6 game grid.
        """
        return [["." for _ in range(self.size)] for _ in range(self.size)]

    def print_board(self, show_ships=False):
        """
        Prints the board with column headers as letters using the chr()
        function to convert numbers to ASCII characters. Numbers are used
        down the side.
        """
        print("   " + " ".join(chr(97 + i) for i in range(self.size)))
        for r in range(self.size):
            row_to_print = [
                '.'
                if cell == 'S' and not show_ships
                else cell for cell in self.grid[r]]
            print(str(r + 1) + "  " + " ".join(row_to_print))

    def place_ships(self):
        """
        Places the ships in random places on the board.
        """
        ships_placed = 0
        while ships_placed < self.num_ships:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.grid[row][col] == ".":
                self.grid[row][col] = "S"
                ships_placed += 1

    def player_guess(self):
        """
        Prompts the player to make their co-ordinate guess. Handles
        the error if the number or letter is not valid or the guess
        is outside of the board size. The column input allows both
        'A' and 'a' inputs. The ord() function is used to get the
        ASCII code of the characters and covert to integers.
        """
        while True:
            try:
                row_input = input("Guess a row: ")
                col_input = input("Guess a column (letter): ").lower()
                row = int(row_input) - 1
                col = ord(col_input) - ord('a')

                if 0 <= row < self.size:
                    if 0 <= col < self.size:
                        return (row, col)
                    else:
                        print(f"Please enter a letter between a and "
                              f"{chr(96 + self.size)}")
                else:
                    print(f"Please enter a number between 1 and "
                          f"{self.size}.")
            except ValueError:
                print("Enter a valid row number and column letter.")

    def valid_guess(self, row, col):
        """
        Checks the guess is valid (i.e on the board and not already
        guessed)
        """
        return self.grid[row][col in [".", "S"]]


player_board= Board()
computer_board= Board()

guess_row, guess_col = player_board.player_guess()

print("Your board:")
player_board.print_board(show_ships=True)
print("\nComputer's board")
computer_board.print_board()
