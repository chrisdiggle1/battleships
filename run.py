import random
import time
from colorama import init, Fore, Style

init(autoreset=True)


class Board:
    def __init__(self, size=6, num_ships=5):
        """
        Initializes the game board with a specific size and places ships
        at random locations.
        """
        self.size = size
        self.num_ships = num_ships
        self.grid = [["." for _ in range(size)] for _ in range(size)]
        self.computer_guesses = set()

    def reinitialise_board(self):
        """
        Creates and returns a new state of the game board.
        """
        return [["." for _ in range(self.size)] for _ in range(self.size)]

    def print_board(self, show_ships=False):
        """
        Prints the board with column headers as letters using the chr()
        function to convert numbers to ASCII characters. Numbers are used
        down the side. Computers ships are hidden.
        """
        print("\n   " + " ".join(chr(97 + i) for i in range(self.size)))
        for r in range(self.size):
            row_to_print = [
                '.'
                if cell == 'S' and not show_ships
                else cell for cell in self.grid[r]]
            print(str(r + 1) + "  " + " ".join(row_to_print))

    def set_ships(self):
        """
        Sets the number of ships based on user input, with a minimum of 2
        and a maximum of 10.
        """
        while True:
            try:
                num_ships = int(input("Enter the number of ships to place on "
                                f"the board (2-10): "))
                if 2 <= num_ships <= 10:
                    self.num_ships = num_ships
                    self.place_ships()
                    break
                else:
                    print(Fore.RED + "Please enter a number between 2 and 10."
                          + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "Invalid input - Please enter a whole "
                      f"number between 2 and 10." + Style.RESET_ALL)

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
        ASCII code of the characters and convert to integers.
        """
        while True:
            col_input = input("\nGuess a column 'a-f':\n").lower()
            if len(col_input) == 1 and 'a' <= col_input <= chr(96 + self.size):
                col = ord(col_input) - ord('a')
                break
            else:
                print(Fore.RED + "Invalid Input - Please enter a single "
                      f" letter between 'a' and '{chr(96 + self.size)}'."
                      + Style.RESET_ALL)

        while True:
            row_input = input("Guess a row '1-6':\n").strip()
            if row_input.isdigit() and len(row_input) == 1:
                row = int(row_input) - 1
                if 0 <= row < self.size:
                    break
                else:
                    print(Fore.RED + "Invalid Input - Please enter a number "
                          f" between '1' and '{self.size}'." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Invalid Input - Please enter a single digit."
                      f" between '1' and '{self.size}'." + Style.RESET_ALL)

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
        Random guess generated for the computers turn.
        """
        while True:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if (row, col) not in self.computer_guesses:
                self.computer_guesses.add((row, col))
                return (row, col)

    def check_game_over(self):
        """
        Checks if all the ships have been hit and the game is finished.
        """
        return all(cell != 'S' for row in self.grid for cell in row)


class GameStats:
    def __init__(self):
        self.games_played = 0
        self.wins = 0
        self.losses = 0
        self.shots_taken = 0
        self.hits = 0
        self.misses = 0

    def shot_stats(self, result):
        """
        Updates the statistics for shots taken, hits, and misses
        based on the result of a guess.
        """
        self.shots_taken += 1
        if result == 'hit':
            self.hits += 1
        else:
            self.misses += 1

    def game_end_stats(self, player_won):
        """
        Updates the game statistics at the end of a game, incrementing
        the count of games playedand recording a win or loss.
        """
        self.games_played += 1
        if player_won:
            self.wins += 1
        else:
            self.losses += 1

    def display_stats(self):
        """
        Prints out the current game statistics including games played,
        wins, losses, total shots taken, hits, misses, and the hit/miss
        ratio.
        """
        hit_miss_ratio = self.hits / max(self.shots_taken, 1)
        print(f"\nGame Statistics:")
        print(f"Games Played: {self.games_played}")
        print(f"Wins: {self.wins}")
        print(f"Losses: {self.losses}")
        print(f"Total Shots Taken: {self.shots_taken}")
        print(f"Hits: {self.hits}")
        print(f"Misses: {self.misses}")
        print(f"Hit/Miss Ratio: {hit_miss_ratio:.2f}")


def display_tutorial():
    """
    Displays the game tutorial with instructions on how to play
    Battleships, including how to guess coordinates and how hits
    and misses are marked.
    """
    print(Fore.CYAN + r"""
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
* You will first be prompted to enter a name which will personalise   *
*  your board, and then you will be asked to select number of ships   *
*  between 2 and 10 that you would like to play, with which will be   *
*  randomly placed on the board for you for each new game.            *
* The game coordinates range from letters 'a' to 'f' along the top    *
* and '1' to '6' down the side. You will be prompted to pick a letter *
* first and then a number. If you hit the computers ship, you         *
* will see a message stating where you hit, and the computers board   *
* will be marked with a '*'. Misses will be marked with 'X' and the   *
* players ships will be marked on their board with an 'S' which will  *
* turn to '*' if hit. all the '.' represents the water. The game will *
* end when one player has sunk all of the other players ships.        *
*                 Good Luck and Enjoy the Game!!                      *
*=====================================================================*
        """ + Style.RESET_ALL)
    input("Press Enter to start the game...\n")
    run_game()


def get_name():
    """
    Prompts the user to enter a name to play game and personalise
    their board with their name. The game will terminate if the user
    enters 'exit'.
    """
    while True:
        name = input(
            "\nPlease enter your name to start the game "
            f"or type 'exit' to quit: ").strip()
        if name == 'exit':
            print("\nExiting the game. Goodbye!")
            exit()
        elif name:
            return name
        else:
            print("\nNo name entered. Please enter a name to continue "
                  f"or type 'exit' to quit.")


def play_or_quit():
    """
    Gives the user to option to quit the game or carry on after each turn.
    If the player enters 'quit' the current game will end.
    """
    quit_game = input("\nPress Enter to continue or type 'quit' to return to "
                      f"the intro screen: ").lower().strip()
    if quit_game == 'quit':
        game_intro()
    else:
        return 'continue'


def run_game():
    """
    Controls the main flow of the game between the player and computer
    taking turns until all of one players ships have been hit. After the
    game ends, the player is asked if they want to play again, and the
    game can be restarted or ended based on their response.
    """
    name = get_name()
    player_board_name = f"{name}'s board"
    game_stats = GameStats()

    while True:
        player_board = Board()
        player_board.set_ships()

        computer_board = Board()
        computer_board.num_ships = player_board.num_ships
        computer_board.place_ships()

        while not player_board.check_game_over() \
                and not computer_board.check_game_over():
            print("\n" + player_board_name + ":\n")
            player_board.print_board(show_ships=True)
            print("\nComputer's board:\n")
            computer_board.print_board()

            # Players turn
            while True:
                guess_row, guess_col = player_board.player_guess()
                if computer_board.valid_guess(guess_row, guess_col):
                    result = computer_board.mark_guess(guess_row, guess_col)
                    game_stats.shot_stats(result)
                    print(f"You {'Hit' if result == 'hit' else 'Missed'} at "
                          f"{chr(97 + guess_col)}{guess_row + 1}!!.")
                    break
                else:
                    print("You've already guessed that spot.")

            if computer_board.check_game_over():
                print("\nComputer's board:")
                computer_board.print_board(show_ships=True)
                print("Congratulations! You have won the game!")
                game_stats.game_end_stats(player_won=True)
                break

            print("\n------------- Player's turn has ended -------------\n")

            # Computers turn
            print("Computer is thinking...")
            time.sleep(2)
            comp_row, comp_col = computer_board.computer_guess()
            result = player_board.mark_guess(comp_row, comp_col)
            game_stats.shot_stats(result)
            print(f"Computer {'Hit' if result == 'hit' else 'Missed'} at "
                  f"{chr(97 + comp_col)}{comp_row + 1}!!.")

            if player_board.check_game_over():
                print("\nYour board:")
                player_board.print_board(show_ships=True)
                print("Sorry, you have lost the game. The computer has won.")
                game_stats.game_end_stats(player_won=False)
                break

            print("\n------------- Computers turn has ended -------------\n")

            if play_or_quit() == 'quit':
                return

        game_stats.display_stats()

        play_again = input(
            "Do you want to play again? (yes/no):\n"
        ).strip().lower()
        if play_again != "yes":
            print("\nThank you for playing Battleships!")
            break


def game_intro():
    """
    Displays the introduction to the game with options to view the tutorial
    or start playing the game. Handles the initial interaction with the user
    """
    print(Fore.CYAN + r"""
 ____        _   _   __             _
(  _ \      ( )_( )_(_ )           ( )    _
| (_) )  _ _|  _)  _)| |   __   ___| |__ (_)_ _    ___
|  _ ( / _  ) | | |  | | / __ \  __)  _  \ |  _ \/  __)
| (_) ) (_| | |_| |_ | |(  ___/__  \ | | | | (_) )__  \
(____/ \__ _)\__)\__)___)\____)____/_) (_)_)  __/(____/
                                           | |
                                           (_)
    """ + Style.RESET_ALL)
    print(Fore.CYAN + r"""
*====================================================*
*               WELCOME TO BATTLESHIPS!!             *
*====================================================*
    """ + Style.RESET_ALL)
    while True:
        choice = input(
            "Press (T) for the Tutorial or (P) to Play The Game:\n"
        ).strip().upper()

        if choice == 'T':
            display_tutorial()
        elif choice == 'P':
            run_game()
            break
        else:
            print(Fore.RED + "Invalid input. Please press 'T' for tutorial or "
                  f"'P' to play." + Style.RESET_ALL)


if __name__ == "__main__":
    game_intro()
