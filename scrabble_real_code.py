from random import shuffle

# ANSI escape codes for colored text
RED_TEXT = "\033[1;31m"
BLUE_TEXT = "\033[0;34m"
LIGHT_BLUE_TEXT = "\033[1;34m"
CYAN_TEXT = "\033[0;36m"
LIGHT_CYAN_TEXT = "\033[1;36m"
YELLOW_TEXT = "\033[0;33m"
RESET_TEXT = "\033[0m"

"""
Scrabble Game Implementation

This script defines classes and functions for a Scrabble game.

Classes:
- Tile: Represents a single tile with a letter and its score.
- Rack: Manages the player's tile rack (their hand of tiles).
- Bag: Represents the pool of tiles available for the game.
- Word: Handles word validation and scoring.
- Board: Manages the Scrabble board, including placement and premium squares.
- Player: Represents a player with a rack, score, and name.

Functions:
- start_game: Initializes the game, including players and the first turn.
- turn: Handles a player's turn, including word placement and turn management.
- end_game: Determines the winner and optionally restarts the game.
"""

# Score values for each letter in the game
LETTER_VALUES = {
    "A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
    "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
    "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10
}

class Tile:
    """
    Represents a single Scrabble tile.

    Attributes:
    - letter: The letter on the tile (uppercase).
    - score: The point value of the letter.

    Methods:
    - get_letter: Returns the tile's letter.
    - get_score: Returns the tile's score.
    """
    def __init__(self, letter, letter_values):
        # Initialize the tile with a letter and its score from LETTER_VALUES.
        self.letter = letter.upper()
        if self.letter in letter_values:
            self.score = letter_values[self.letter]
        else:
            self.score = 0

    def get_letter(self):
        return self.letter

    def get_score(self):
        return self.score

class Bag:
    """
    Represents the bag containing all Scrabble tiles.

    Methods:
    - add_to_bag: Adds a specified quantity of a tile to the bag.
    - initialize_bag: Fills the bag with the default distribution of tiles.
    - take_from_bag: Removes and returns a random tile from the bag.
    - get_remaining_tiles: Returns the count of remaining tiles.
    """
    def __init__(self):
        #Creates the bag full of game tiles, and calls the initialize_bag() method, which adds the default 100 tiles to the bag.
        #Takes no arguments.
        self.bag = [] # List to store tiles
        self.initialize_bag()

    def add_to_bag(self, tile, quantity):
        #Adds a certain quantity of a certain tile to the bag. Takes a tile and an integer quantity as arguments.
        for i in range(quantity):
            self.bag.append(tile)

    def initialize_bag(self):
        # Add tiles to the bag based on the standard Scrabble distribution.
        global LETTER_VALUES
        self.add_to_bag(Tile("A", LETTER_VALUES), 9)
        self.add_to_bag(Tile("B", LETTER_VALUES), 2)
        self.add_to_bag(Tile("C", LETTER_VALUES), 2)
        self.add_to_bag(Tile("D", LETTER_VALUES), 4)
        self.add_to_bag(Tile("E", LETTER_VALUES), 12)
        self.add_to_bag(Tile("F", LETTER_VALUES), 2)
        self.add_to_bag(Tile("G", LETTER_VALUES), 3)
        self.add_to_bag(Tile("H", LETTER_VALUES), 2)
        self.add_to_bag(Tile("I", LETTER_VALUES), 9)
        self.add_to_bag(Tile("J", LETTER_VALUES), 9)
        self.add_to_bag(Tile("K", LETTER_VALUES), 1)
        self.add_to_bag(Tile("L", LETTER_VALUES), 4)
        self.add_to_bag(Tile("M", LETTER_VALUES), 2)
        self.add_to_bag(Tile("N", LETTER_VALUES), 6)
        self.add_to_bag(Tile("O", LETTER_VALUES), 8)
        self.add_to_bag(Tile("P", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Q", LETTER_VALUES), 1)
        self.add_to_bag(Tile("R", LETTER_VALUES), 6)
        self.add_to_bag(Tile("S", LETTER_VALUES), 4)
        self.add_to_bag(Tile("T", LETTER_VALUES), 6)
        self.add_to_bag(Tile("U", LETTER_VALUES), 4)
        self.add_to_bag(Tile("V", LETTER_VALUES), 2)
        self.add_to_bag(Tile("W", LETTER_VALUES), 2)
        self.add_to_bag(Tile("X", LETTER_VALUES), 1)
        self.add_to_bag(Tile("Y", LETTER_VALUES), 2)
        self.add_to_bag(Tile("Z", LETTER_VALUES), 1)
        shuffle(self.bag)

    def take_from_bag(self):
        # Draws a tile from the bag. If the bag is nearly empty, refill it.
        if len(self.bag) < 10:  
            self.initialize_bag()  
        return self.bag.pop()

    def get_remaining_tiles(self):
        #Returns the number of tiles left in the bag.
        return len(self.bag)
        

class Rack:
    """
    Represents a player's rack (hand of tiles).

    Methods:
    - add_to_rack: Draws a tile from the bag and adds it to the rack.
    - initialize: Fills the rack with the initial 7 tiles.
    - get_rack_str: Returns a string representation of the rack.
    - get_rack_arr: Returns the rack as a list of tile objects.
    - remove_from_rack: Removes a specified tile from the rack.
    - replenish_rack: Refills the rack to 7 tiles if possible.
    - shuffle_rack: Randomly rearranges the tiles in the rack.
    """
    def __init__(self, bag):
        self.rack = []  # List to store the player's tiles
        self.bag = bag
        self.initialize()

    def add_to_rack(self):
        self.rack.append(self.bag.take_from_bag())

    def initialize(self):
        for i in range(7):
            self.add_to_rack()

    def get_rack_str(self):
        # Returns the rack as a comma-separated string with colored letters.
        return ", ".join(f"{YELLOW_TEXT}{str(item.get_letter())}{RESET_TEXT}" for item in self.rack)

    def get_rack_arr(self):
        return self.rack

    def remove_from_rack(self, tile):
        self.rack.remove(tile)

    def get_rack_length(self):
        return len(self.rack)

    def replenish_rack(self):
        while self.get_rack_length() < 7 and self.bag.get_remaining_tiles() > 0:
            self.add_to_rack()
     
    def shuffle_rack(self):
        shuffle(self.rack)
        

class Player:
    """
    Represents a Scrabble player.

    Attributes:
    - name: The player's name.
    - rack: The player's rack of tiles (instance of Rack).
    - score: The player's current score.

    Methods:
    - set_name: Sets the player's name.
    - get_name: Retrieves the player's name.
    - get_rack_str: Returns the player's rack as a formatted string.
    - get_rack_arr: Returns the player's rack as a list of Tile objects.
    - increase_score: Adds points to the player's score.
    - get_score: Retrieves the player's current score.
    """
    def __init__(self, bag):
        # Initialize a player with an empty name, a rack from the given bag, and a score of 0.
        self.name = ""
        self.rack = Rack(bag)
        self.score = 0

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_rack_str(self):
        return self.rack.get_rack_str()

    def get_rack_arr(self):
        return self.rack.get_rack_arr()

    def increase_score(self, increase):
        self.score += increase

    def get_score(self):
        return self.score

class Board:
    """
    Represents the Scrabble board.

    Attributes:
    - board: A 15x15 grid initialized with empty spaces and premium square indicators.

    Methods:
    - get_board: Returns a formatted string representation of the board.
    - add_premium_squares: Adds premium squares (e.g., double/triple word/letter scores) to the board.
    - place_word: Places a word on the board and updates the player's rack.
    - board_array: Returns the raw 2D array representation of the board.
    """
    def __init__(self):
        # Initialize a 15x15 board and add premium squares.
        self.board = [["   " for i in range(15)] for j in range(15)]
        self.add_premium_squares()
        self.board[7][7]  = f"{RED_TEXT} * {RESET_TEXT}"

    def get_board(self):
        # Returns the board as a formatted string for display.
        board_str = "   |  " + "  |  ".join(str(item) for item in range(10)) + "  | " + "  | ".join(str(item) for item in range(10, 15)) + " |"
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _\n"
        board = list(self.board)
        for i in range(len(board)):
            if i < 10:
                board[i] = str(i) + "  | " + " | ".join(str(item) for item in board[i]) + " |"
            if i >= 10:
                board[i] = str(i) + " | " + " | ".join(str(item) for item in board[i]) + " |"
        board_str += "\n   |_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _|\n".join(board)
        board_str += "\n   _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _"
        return board_str

    def add_premium_squares(self):
        # Adds premium squares (e.g., TWS, DWS, TLS, DLS) to the board.
        TRIPLE_WORD_SCORE = ((0,0), (7, 0), (14,0), (0, 7), (14, 7), (0, 14), (7, 14), (14,14))
        DOUBLE_WORD_SCORE = ((1,1), (2,2), (3,3), (4,4), (1, 13), (2, 12), (3, 11), (4, 10), (13, 1), (12, 2), (11, 3), (10, 4), (13,13), (12, 12), (11,11), (10,10))
        TRIPLE_LETTER_SCORE = ((1,5), (1, 9), (5,1), (5,5), (5,9), (5,13), (9,1), (9,5), (9,9), (9,13), (13, 5), (13,9))
        DOUBLE_LETTER_SCORE = ((0, 3), (0,11), (2,6), (2,8), (3,0), (3,7), (3,14), (6,2), (6,6), (6,8), (6,12), (7,3), (7,11), (8,2), (8,6), (8,8), (8, 12), (11,0), (11,7), (11,14), (12,6), (12,8), (14, 3), (14, 11))

        for coordinate in TRIPLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = f"{LIGHT_BLUE_TEXT}TWS{RESET_TEXT}"
        for coordinate in TRIPLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = f"{BLUE_TEXT}TLS{RESET_TEXT}"
        for coordinate in DOUBLE_WORD_SCORE:
            self.board[coordinate[0]][coordinate[1]] = f"{LIGHT_CYAN_TEXT}DWS{RESET_TEXT}"
        for coordinate in DOUBLE_LETTER_SCORE:
            self.board[coordinate[0]][coordinate[1]] = f"{CYAN_TEXT}DLS{RESET_TEXT}"
            

    def place_word(self, word, location, direction, player):
        # Places a word on the board and updates the player's rack.
        global premium_spots
        premium_spots = []
        direction = direction.lower()
        word = word.upper()
        
        # Place the word horizontally
        if direction.lower() == "right":
            for i in range(len(word)):
                if self.board[location[0]][location[1]+i] != "   ":
                    premium_spots.append((word[i], self.board[location[0]][location[1]+i]))
                self.board[location[0]][location[1]+i] = f" {RED_TEXT}{word[i]}{RESET_TEXT} "

        # Place the word vertically
        elif direction.lower() == "down":
            for i in range(len(word)):
                if self.board[location[0]][location[1]+i] != "   ":
                    premium_spots.append((word[i], self.board[location[0]][location[1]+i]))
                self.board[location[0]+i][location[1]] = f" {RED_TEXT}{word[i]}{RESET_TEXT} "

        # Update player's rack by removing used tiles
        for letter in word:
            for tile in player.get_rack_arr():
                if tile.get_letter() == letter:
                    player.rack.remove_from_rack(tile)
        player.rack.replenish_rack()

    def board_array(self):
        #Returns the 2-dimensional board array.
        return self.board

class Word:
    """
    Handles validation and scoring of words in the Scrabble game.
    """

    def __init__(self, word, location, player, direction, board):
        self.word = word.upper() # Store the word in uppercase
        self.location = location # Starting location of the word on the board (row, col)
        self.player = player  # The player placing the word
        self.direction = direction.lower() # Direction of the word ("right" or "down")
        self.board = board  # The game board

    def check_word(self):
        """
        Validates the word for correct placement, overlap, and dictionary presence.

        Validation steps:
        1. Ensures the word is placed in a valid direction (right or down).
        2. Confirms the word exists in the dictionary.
        3. Checks overlapping letters on the board for consistency with the word being played.
        4. Ensures the word connects to existing letters on the board (after the first round).
        5. Validates the player has all necessary tiles to play the word.
        6. Checks the word fits within the board boundaries.
        7. Ensures the first word is placed at the center of the board (7,7).

        Returns:
        - True: If the word passes all validation checks.
        - str: Error message describing why the word is invalid.
        """
        global round_number, players
        global dictionary
        word_score = 0

        # Initialize variables for validation
        current_board_ltr = ""  # Letters already on the board that the word overlaps with
        needed_tiles = ""  # Tiles the player needs to complete the word

        # Load the dictionary if not already loaded
        if "dictionary" not in globals():
            dictionary = open("dic.txt").read().splitlines()

        # Validate word placement only if the word is not empty
        if self.word != "":
            # Check the direction of the word placement
            if self.direction == "right":
                for i in range(len(self.word)):
                    board_tile = self.board[self.location[0]][self.location[1] + i]
                    if board_tile.strip() in ["", "TWS", "DWS", "TLS", "DLS", "*"]:
                        current_board_ltr += " " # Empty or premium square
                    else:
                        current_board_ltr += board_tile.strip()[1]   # Extract existing letter
            elif self.direction == "down":
                for i in range(len(self.word)):
                    board_tile = self.board[self.location[0] + i][self.location[1]]
                    if board_tile.strip() in ["", "TWS", "DWS", "TLS", "DLS", "*"]:
                        current_board_ltr += " " 
                    else:
                        current_board_ltr += board_tile.strip()[1]  # Extract existing letter on board
            else:
                return "Error: Please enter a valid direction (right or down)."

            # Validate that the word exists in the dictionary
            if self.word not in dictionary:
                return "Please enter a valid dictionary word.\n"

            # Ensure overlapping letters on the board match the word being played
            if self.direction == "right":
                for i, letter in enumerate(self.word):
                    self.board[self.location[0]][self.location[1] + i] # Update board
            elif self.direction == "down":
                for i, letter in enumerate(self.word):
                    self.board[self.location[0] + i][self.location[1]] # Update board
                    
            # Check if the word connects to existing letters on the board (after the first round)
            if round_number > 1 and current_board_ltr == " " * len(self.word):
                return "The word must connect to an existing letter on the board."

            # Verify the player has all necessary tiles to play the word
            for letter in needed_tiles:
                if self.player.get_rack_str().count(letter) < needed_tiles.count(letter):
                    return f"You do not have the necessary tiles to play the word '{self.word}'."

            # Ensure the word fits within the board boundaries
            if (
                self.location[0] < 0
                or self.location[1] < 0
                or (self.direction == "right" and self.location[1] + len(self.word) > 15)
                or (self.direction == "down" and self.location[0] + len(self.word) > 15)
            ):
                return "The word placement is out of bounds."

            # Verify the first word is placed at the center of the board (7,7)
            if round_number == 1 and players[0] == self.player and self.location != [7, 7]:
                return "The first word must begin at the center of the board (7, 7)."

            return True


    def calculate_word_score(self):
        """
        Calculates the score of the word, including premium square bonuses.

        Scoring Details:
        - Each letter has a base score determined by LETTER_VALUES.
        - Letter bonus squares (TLS, DLS) multiply the scores of individual letters.
        - Word bonus squares (TWS, DWS) multiply the total word score.
        """
        global LETTER_VALUES, premium_spots
        word_score = 0
        
        # Add base score for each letter and apply any applicable letter bonuses
        for letter in self.word:
            for spot in premium_spots:
                if letter == spot[0]:
                    if spot[1] == "TLS":
                        word_score += LETTER_VALUES[letter] * 2
                    elif spot[1] == "DLS":
                        word_score += LETTER_VALUES[letter]
            word_score += LETTER_VALUES[letter]
            
        # Apply word multipliers from premium squares
        for spot in premium_spots:
            if spot[1] == "TWS":
                word_score *= 3
            elif spot[1] == "DWS":
                word_score *= 2
                
        # Update the player's score
        self.player.increase_score(word_score)

    # Setter and getter methods for the word's attributes
    def set_word(self, word):
        self.word = word.upper()

    def set_location(self, location):
        self.location = location

    def set_direction(self, direction):
        self.direction = direction

    def get_word(self):
        return self.word

def turn(player, board, bag):
    """
    Manages a player's turn, including displaying the board, handling input,
    and progressing to the next player's turn.

    Purpose:
    - Displays the current state of the board and the player's rack.
    - Provides a menu of actions (e.g., shuffle rack, renew rack, play a word).
    - Handles the process of placing a word, including validation and scoring.
    - Updates the game state and moves to the next player's turn or ends the game.
    """
    global round_number, players, skipped_turns

    # Check if the game should continue based on skipped turns and tiles
    if (skipped_turns < 6) or (player.rack.get_rack_length() == 0 and bag.get_remaining_tiles() == 0):

        # Display round and player info
        print("\nRound " + str(round_number) + ": " + player.get_name() + "'s turn \n")
        print(board.get_board())

        # Player actions menu
        while True:
            print(player.get_name() + "'s Letter Rack: " + player.get_rack_str() + "\n")
            print("Command List")
            print("Press 1 to continue the game")
            print("Press 2 to shuffle rack")
            print("Press 3 to renew rack")
            print("Press 4 to skip turn")
            print("Press 5 to exit game" + "\n")
            
            numm = input().strip()
            if numm == "1":
                break

            elif numm == "2":
                player.rack.shuffle_rack()
                print("\n\n" + board.get_board())
                print("\n" + "Your rack has been shuffled!")

            elif numm == "3":
                player.rack.rack.clear()
                player.rack.replenish_rack()
                print("\n\n" + board.get_board())
                print("\n" + "Your rack has been renewed!")
                
            
            elif numm == "4":
                print("are you sure to skip your turn? (y/n)")
                answer = input().strip().lower()
                if answer == "n":
                    print("\n")
                    continue
                elif answer == "y":
                    word_to_play = ""
                    skipped_turns += 1
                    if players.index(player) != (len(players)-1):
                        player = players[players.index(player)+1]
                    else:
                        player = players[0]
                        round_number += 1
                    turn(player, board, bag)
                    return
                else:
                    print("\n" + f"{RED_TEXT}please input a valid option{RESET_TEXT}")



            elif numm == "5":
                print("are you sure to exit the game? (y/n)")
                answerr = input().strip().lower()
                if answerr == "n":
                    print("\n")
                    continue
                elif answerr == "y":
                    print("thankyou for playing")
                    exit()
                else:
                    print("\n" + f"{RED_TEXT}please input a valid option{RESET_TEXT}")
                
            else:
                print("\n\n" + board.get_board())
                print("\n" + f"{RED_TEXT}please input a valid option{RESET_TEXT}")

        # Get word placement info from the player
        word_to_play = input("Word to play: ")
        location = []
        col = input("Column number: ")
        row = input("Row number: ")
        if (col == "" or row == "") or (col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
            location = [-1, -1]
        else:
            location = [int(row), int(col)]
        direction = input("Direction of word (right or down): ")

        word = Word(word_to_play, location, player, direction, board.board_array())

        #If the word throws an error, creates a recursive loop until the information is given correctly.
        checked = word.check_word()
        while checked != True:
            print(checked)
            word_to_play = input("Word to play: ")
            word.set_word(word_to_play)
            location = []
            col = input("Column number: ")
            row = input("Row number: ")
            if (col == "" or row == "") or (col not in [str(x) for x in range(15)] or row not in [str(x) for x in range(15)]):
                location = [-1, -1]
            else:
                word.set_location([int(row), int(col)])
                location = [int(row), int(col)]
            direction = input("Direction of word (right or down): ")
            word.set_direction(direction)
            checked = word.check_word()

        # Place the word and update the game state
        board.place_word(word_to_play, location, direction, player)
        word.calculate_word_score()
        skipped_turns = 0

        #Prints the current player's score
        print("\n" + player.get_name() + "'s score is: " + str(player.get_score()))

        #Gets the next player.
        if players.index(player) != (len(players)-1):
            player = players[players.index(player)+1]
        else:
            player = players[0]
            round_number += 1

        #Recursively calls the function in order to play the next turn.
        turn(player, board, bag)

    #If the number of skipped turns is over 6 or the bag has both run out of tiles and a player is out of tiles, end the game.
    else:
        end_game()

def start_game():
    """
    Initializes the game, including player setup, and starts the first turn.

    Purpose:
    - Sets up the game state, including the board, bag, and players.
    - Prompts players for their names and initializes their racks.
    - Begins the first round of the game with player 1's turn.
    """
    global round_number, players, skipped_turns
    board = Board()
    bag = Bag()

    # Get number of players
    while True:
        try:
            num_of_players = int(input("Please enter the number of players (2-4): "))
            if num_of_players in [2, 3, 4]:
                break  # Exit the loop if the input is valid
            else:
                print("This number is invalid. Please enter the number of players (2-4).")
        except ValueError:
            print("Invalid input. Please enter a number (2-4).")


    # Setup players
    print("\nWelcome to Scrabble! Please enter the names of the players below.")
    players = []
    for i in range(num_of_players):
        players.append(Player(bag))
        players[i].set_name(input("Please enter player " + str(i+1) + "'s name: "))

    # Initialize game variables
    round_number = 1
    skipped_turns = 0
    current_player = players[0]
    turn(current_player, board, bag)

def end_game():
    """
    Ends the game, announces the winner, and optionally restarts the game.

    Purpose:
    - Determines the winner(s) based on the highest score.
    - Displays the scores and winner(s).
    - Provides an option to restart or exit the game.
    """
    global players
    
    # Determine the winner
    highest_score = 0
    winning_player = ""
    for player in players:
        if player.get_score > highest_score:
            highest_score = player.get_score()
            winning_player = player.get_name()
    print("The game is over! " + winning_player + ", you have won!")

    if input("\nWould you like to play again? (y/n)").upper() == "Y":
        start_game()

start_game()