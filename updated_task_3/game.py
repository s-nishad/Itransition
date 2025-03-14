import sys
import random
from dice import Dice
from fair_random_generator import FairRandomGenerator
from probability_calculator import ProbabilityCalculator
from help_table_generator import HelpTableGenerator

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
        available_dice = [die for die in self.dice if die != self.computer_dice]
        for i, die in enumerate(available_dice):
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
                if user_index < 0 or user_index >= len(available_dice):
                    print("Invalid input. Please enter a valid dice index.")
                    continue
                self.user_dice = available_dice[user_index]
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