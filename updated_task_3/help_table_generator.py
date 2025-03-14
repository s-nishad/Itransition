from tabulate import tabulate
from colorama import Fore, Style
from probability_calculator import ProbabilityCalculator

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