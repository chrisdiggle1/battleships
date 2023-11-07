import random
import time


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

    def reinitialise_board(self):
        """
        resets the game board to its initial state, clearing any previous
        game state.
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
            col_input = input("Guess a column 'a-f':\n").lower()
            if len(col_input) == 1 and 'a' <= col_input <= chr(96 + self.size):
                col = ord(col_input) - ord('a')
                break
            else:
                print(f"Invalid Letter - Please enter a single letter "
                      f"between 'a' and '{chr(96 + self.size)}'.")

        while True:
            row_input = input("Guess a row '1-6':\n").strip()
            if row_input.isdigit() and len(row_input) == 1:
                row = int(row_input) - 1
                if 0 <= row < self.size:
                    break
                else:
                    print(f"Invalid Number - Please enter a number between "
                          f" '1' and '{self.size}'.")
            else:
                print("Invalid input - Please enter a single digit.")

        return row, col

    def valid_guess(self, row, col):
        """
        Checks the guess is valid (i.e on the board and not already
        guessed)
        """
        return self.grid[row][col] in [".", "S"]

    def mark_guess(self, row, col):
        """
        Mark the board with a hit or miss depending on the players guess.
        '*' marks a hit and 'X' marks a miss"
        """
        if self.grid[row][col] == "S":
            self.grid[row][col] = "*"
            return "hit"
        else:
            self.grid[row][col] = "X"
            return "miss"

    def computer_guess(self):
        """
        Random guess generated for the computers turn
        """
        while True:
            col = random.randint(0, self.size - 1)
            row = random.randint(0, self.size - 1)
            if self.grid[row][col] in [".", "S"]:
                return (row, col)

    def check_game_over(self):
        """
        Checks if all the ships have been hit and the game is finished.
        """
        return all(cell != 'S' for row in self.grid for cell in row)


def display_tutorial():
    """
    Displays the game tutorial with instructions on how to play.
    """
    print(r"""
* ====================================================================*
*                                                                     *
*                           Battleships                               *
*=====================================================================*
* Welcome to Battleships, the classic naval combat game where strategy*
* meets suspense! Prepare to engage in a thrilling war of wits, as    *
* you pit your fleet against the unseen enemy. The objective is       *
* simple, yet achieving it will require cunning, coordination, and a  *
* little bit of luck. Get ready to embark on a high-seas adventure    *
* where only the most astute commanders will prevail. Set your sights *
* on victory, captain, for the battle is about to begin!              *
*=====================================================================*
*
* The game coordinates range from letters 'a' to 'f' along the top    *
* and '1' to '6' down the side. You will be prompted to pick a letter *
* first and then a letter after that. If you hit the computers ship,  *
* you will see a message stating where you hit and the computers      *
* will be marked with a '*'. Misses will be marked with 'X' and the   *
* players ships will be marked on their board with an 'S' which will  *
* turn to '*' if hit. all the '.' represents the water. The game will *
* end when one player has sunk all 5 of the other players ships.      *
*                 Good Luck and Enjoy the Game!!                      *
*=====================================================================*
        """)
    input("Press Enter to start the game...\n")
    run_game()


def run_game():
    """
    Controls the main flow of the game between the player and computer
    and handles the play again function once the current game has finished.
    """
    player_board = Board()
    computer_board = Board()

    while True:
        print("Your board:")
        player_board.print_board(show_ships=True)
        print("\nComputer's board:")
        computer_board.print_board()

        # Players turn
        while True:
            guess_row, guess_col = player_board.player_guess()
            if computer_board.valid_guess(guess_row, guess_col):
                result = computer_board.mark_guess(guess_row, guess_col)
                print(f"You {'Hit' if result == 'hit' else 'Missed'} at "
                      f"{chr(97 + guess_col)}{guess_row + 1}!!.")
                break
            else:
                print("You've already guessed that spot.")

        if computer_board.check_game_over():
            print("\nComputer's board:")
            computer_board.print_board()
            return "Player"

        print("\n------------- Player's turn has ended -------------\n")

        # Computers turn
        print("Computer is thinking...")
        time.sleep(2)
        comp_row, comp_col = player_board.computer_guess()
        result = player_board.mark_guess(comp_row, comp_col)
        print(f"Computer {'Hit' if result == 'hit' else 'Missed'} at "
              f"{chr(97 + comp_col)}{comp_row + 1}!!.")

        if player_board.check_game_over():
            print("\nYour board:")
            player_board.print_board(show_ships=True)
            return "Computer"

        print("\n--------------- Computers turn has ended ---------------\n")


def game_intro():
    while True:
        """
        Displays the introduction to the game using ASCII art and gives the
        userthe option of viewing a tutorial or playing the game.
        """
        print(r"""
 ____        _   _   __             _
(  _ \      ( )_( )_(_ )           ( )    _
| (_) )  _ _|  _)  _)| |   __   ___| |__ (_)_ _    ___
|  _ ( / _  ) | | |  | | / __ \  __)  _  \ |  _ \/  __)
| (_) ) (_| | |_| |_ | |(  ___/__  \ | | | | (_) )__  \
(____/ \__ _)\__)\__)___)\____)____/_) (_)_)  __/(____/
                                           | |
                                           (_)
        """)
        print(r"""
 ====================================================
*               WELCOME TO BATTLESHIPS!!             *
*====================================================*
        """)
        choice = input(
            "Press (T) for the Tutorial or (P) to Play The Game:\n"
        ).strip().upper()

        if choice == 'T':
            display_tutorial()
        elif choice == 'P':
            winner = run_game()
            if winner == "Player":
                print("Congratulations! You have won the game!")
            elif winner == "Computer":
                print("Sorry, you have lost the game. The computer has won.")

            play_again = input(
                "Do you want to play again? (yes/no):\n"
            ).strip().lower()
            if play_again != "yes":
                print("Thank you for playing Battleships!")
                break
        else:
            print("Invalid input. Please press 'T' for tutorial or 'P' to "
                  " play.")


if __name__ == "__main__":
    game_intro()
