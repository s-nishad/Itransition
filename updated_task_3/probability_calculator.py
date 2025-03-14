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