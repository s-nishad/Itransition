import sys
from dice_parser import DiceParser
from game import Game

if __name__ == "__main__":
    try:
        dice = DiceParser.parse(sys.argv[1:])
        game = Game(dice)
        game.play()
    except ValueError as e:
        print(f"Error: {e}")
        print("Example usage: python main.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3")
