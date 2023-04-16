import random

class RandomSequence():
    def __init__(self, sequence, history=1):
        self.sequence = sequence
        self.pending = list(sequence)
        self.history = [None] * history

    def get_next(self):
        if not self.pending:
            self.pending = list(self.sequence)

        # Filter elements based on constraint
        candidates = [x for x in self.pending if x not in self.history]

        # Choose a random element from the candidates
        selected = random.choice(candidates)

        # Update the list of pending elements and the history
        self.pending.remove(selected)
        self.history.pop(0)
        self.history.append(selected)

        return selected
