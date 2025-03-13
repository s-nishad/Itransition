import sys
import random
import hmac
import hashlib
from tabulate import tabulate
from colorama import Fore, Style

# Dice class to represent a die with its faces
class Dice:
    def __init__(self, faces):
        self.faces = faces

    def roll(self):
        return random.choice(self.faces)

    def __str__(self):
        return ",".join(map(str, self.faces))


# DiceParser class to parse dice configurations from command-line arguments
class DiceParser:
    @staticmethod
    def parse(args):
        if len(args) < 3:
            raise ValueError("At least 3 dice are required.")
        dice = []
        for arg in args:
            try:
                faces = list(map(int, arg.split(",")))
                dice.append(Dice(faces))
            except ValueError:
                raise ValueError(f"Invalid dice configuration: {arg}. Expected comma-separated integers.")
        return dice


# FairRandomGenerator class for fair random number generation using HMAC
class FairRandomGenerator:
    def __init__(self, range_max):
        self.range_max = range_max
        self.key = random.randbytes(32)  # 256-bit key
        self.computer_number = random.randint(0, range_max)
        self.hmac = self._calculate_hmac()

    def _calculate_hmac(self):
        return hmac.new(self.key, str(self.computer_number).encode(), hashlib.sha3_256).hexdigest()

    def get_hmac(self):
        return self.hmac

    def get_result(self, user_number):
        result = (self.computer_number + user_number) % (self.range_max + 1)
        return result, self.key.hex()


# ProbabilityCalculator class to calculate win probabilities between dice
class ProbabilityCalculator:
    @staticmethod
    def calculate_probability(dice1, dice2):
        wins = 0
        for face1 in dice1.faces:
            for face2 in dice2.faces:
                if face1 > face2:
                    wins += 1
        total = len(dice1.faces) * len(dice2.faces)
        return wins / total


# HelpTableGenerator class to display the probability table
class HelpTableGenerator:
    @staticmethod
    def generate_table(dice):
        description = (
            "This table shows the probability of one die winning against another.\n"
            "Each cell represents the probability that the row die beats the column die.\n"
            "The diagonal cells (marked with '-') indicate that a die cannot play against itself.\n"
        )
        print(description)

        # Use dice values as headers and row labels
        headers = [Fore.BLUE + "User Dice \\ Computer Dice" + Style.RESET_ALL] + [
            Fore.GREEN + str(die) + Style.RESET_ALL for die in dice
        ]
        table = []
        for i, die1 in enumerate(dice):
            row = [Fore.GREEN + str(die1) + Style.RESET_ALL]  # Use dice value as row label
            for j, die2 in enumerate(dice):
                if i == j:
                    row.append(Fore.RED + "-" + Style.RESET_ALL)  # Diagonal cells
                else:
                    prob = ProbabilityCalculator.calculate_probability(die1, die2)
                    row.append(f"{prob:.4f}")
            table.append(row)
        print(tabulate(table, headers, tablefmt="grid"))


# Game class to manage the game flow
class Game:
    def __init__(self, dice):
        self.dice = dice
        self.current_player = None
        self.computer_dice = None
        self.user_dice = None

    def determine_first_player(self):
        print("Let's determine who makes the first move.")
        fair_random = FairRandomGenerator(1)
        print(f"I selected a random value in the range 0..1 (HMAC={fair_random.get_hmac()}).")
        print("Try to guess my selection.")
        print("0 - 0")
        print("1 - 1")
        print("X - exit")
        print("? - help")
        while True:
            user_choice = input("Your selection: ").strip().lower()
            if user_choice == "x":
                sys.exit(0)
            elif user_choice == "?":
                HelpTableGenerator.generate_table(self.dice)
                continue
            try:
                user_number = int(user_choice)
                if user_number not in [0, 1]:
                    print("Invalid input. Please enter 0, 1, X, or ?.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter 0, 1, X, or ?.")
        result, key = fair_random.get_result(user_number)
        print(f"My selection: {result} (KEY={key}).")
        self.current_player = "user" if result == user_number else "computer"
        print(f"{self.current_player.capitalize()} makes the first move.")

    def select_dice(self):
        if self.current_player == "computer":
            self.computer_dice = random.choice(self.dice)
            print(f"I choose the [{self.computer_dice}] dice.")
        print("Choose your dice:")
        for i, die in enumerate(self.dice):
            print(f"{i} - {die}")
        print("X - exit")
        print("? - help")
        while True:
            user_choice = input("Your selection: ").strip().lower()
            if user_choice == "x":
                sys.exit(0)
            elif user_choice == "?":
                HelpTableGenerator.generate_table(self.dice)
                continue
            try:
                user_index = int(user_choice)
                if user_index < 0 or user_index >= len(self.dice):
                    print("Invalid input. Please enter a valid dice index.")
                    continue
                self.user_dice = self.dice[user_index]
                print(f"You choose the [{self.user_dice}] dice.")
                break
            except ValueError:
                print("Invalid input. Please enter a valid dice index, X, or ?.")

    def roll_dice(self, dice):
        fair_random = FairRandomGenerator(len(dice.faces) - 1)
        print(f"I selected a random value in the range 0..{len(dice.faces) - 1} (HMAC={fair_random.get_hmac()}).")
        print("Add your number modulo 6.")
        for i in range(len(dice.faces)):
            print(f"{i} - {i}")
        print("X - exit")
        print("? - help")
        while True:
            user_choice = input("Your selection: ").strip().lower()
            if user_choice == "x":
                sys.exit(0)
            elif user_choice == "?":
                HelpTableGenerator.generate_table(self.dice)
                continue
            try:
                user_number = int(user_choice)
                if user_number < 0 or user_number >= len(dice.faces):
                    print("Invalid input. Please enter a valid number.")
                    continue
                result, key = fair_random.get_result(user_number)
                print(f"My number is {fair_random.computer_number} (KEY={key}).")
                print(f"The result is {fair_random.computer_number} + {user_number} = {result} (mod {len(dice.faces)}).")
                return dice.faces[result]
            except ValueError:
                print("Invalid input. Please enter a valid number, X, or ?.")

    def play(self):
        self.determine_first_player()
        self.select_dice()
        
        if self.current_player == "computer":
            # Computer rolls first
            computer_roll = self.roll_dice(self.computer_dice)
            print(f"My throw is {computer_roll}.")
            user_roll = self.roll_dice(self.user_dice)
            print(f"Your throw is {user_roll}.")
        else:
            # User rolls first
            user_roll = self.roll_dice(self.user_dice)
            print(f"Your throw is {user_roll}.")
            
            # Computer selects a dice after the user selects theirs
            available_dice = [die for die in self.dice if die != self.user_dice]
            self.computer_dice = random.choice(available_dice)
            print(f"I choose the [{self.computer_dice}] dice.")
            
            # Computer rolls its dice
            computer_roll = self.roll_dice(self.computer_dice)
            print(f"My throw is {computer_roll}.")
        
        # Determine the winner
        if user_roll > computer_roll:
            print(f"You win ({user_roll} > {computer_roll})!")
        elif user_roll < computer_roll:
            print(f"I win ({computer_roll} > {user_roll})!")
        else:
            print("It's a tie!")


# Main entry point
if __name__ == "__main__":
    try:
        dice = DiceParser.parse(sys.argv[1:])
        game = Game(dice)
        game.play()
    except ValueError as e:
        print(f"Error: {e}")
        print("Example usage: python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")