from dice import Dice

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