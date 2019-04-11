from Gap import Gap
from random import random, choice, randint, shuffle

"""
    The ant moves from Gap to Gap, stepping from a Word to the next Gap to be matched is random
    Only stepping from a Gap to a Word is computed
"""
class Ant:
    def __init__(self, gaps, words, trace, alpha, beta, q0):
        # pairs (Gap, Word)
        self.path = []
        self.gaps = gaps
        self.gap_ids = [gap.id for gap in gaps]
        shuffle([self.gap_ids])

        # marks the gap we;re trying to match to a word when update() is called
        self.currentGap_idx = 0

        self.words = words
        self.startingPath = "gap"
        self.trace = trace
        self.alpha = alpha
        self.beta = beta
        self.q0 = q0
        # the length of the solution (no. of edges)
        self.solSize = len(self.trace)*2-1

    """
    On each update the ant will pick a node and step to it, updating its travelled path
    """
    def update(self):
        nextSteps = []

        # how well the key word will fit in the current gap
        # computed for each of the available word (that are not matched to a gap yet)
        visibility = {}

        nextSteps = self.nextMoves()

        # return if there are any moves to do
        if len(nextSteps) == 0 or self.gap_ids[self.currentGap_idx] == len(self.gaps):
            return

        # associate each of the next moves with empirical distance
        for stepWord in nextSteps:
            tmp = [gap for gap in self.gaps if gap.id == self.gap_ids[self.currentGap_idx]]
            if len(tmp) == 0:
                return
            visibility[stepWord] = self.matching(stepWord, tmp[0])

        # trace^alpha + viz^beta
        for word in visibility.keys():
            visibility[word] = self.trace[self.gap_ids[self.currentGap_idx]][word.id]**self.alpha + visibility[word]**self.beta

        if random() < self.q0:
            # add the best of the nextSteps to the path
            best = max(visibility.keys(), key=lambda w: visibility[w])
            current_gap = [gap for gap in self.gaps if gap.id == self.gap_ids[self.currentGap_idx]][0]

            self.path.append((current_gap, best))

            self.currentGap_idx += 1 # next gap
        else:
            # add a random word to the path, a word that fits
            current_gap = [gap for gap in self.gaps if gap.id == self.gap_ids[self.currentGap_idx]][0]
            fitting_words = [word for word in self.nextMoves() if len(word.word) == current_gap.size]

            if fitting_words == []:
                return

            picked = fitting_words[randint(0, len(fitting_words)-1)]

            self.path.append((current_gap, picked))
            self.currentGap_idx += 1 # next gap


    """
    Return the number of restrictions satisfied by using word on the next position and if the size fits
    if it doesn't, return 0
    """
    def matching(self, word, gap):
        if gap.size != len(word.word):
            # doesn't fit, minimum matching
            return 0

        # count the number of restrictions fulfilled by word.word
        restrictions_matched = sum([1 for restriction in gap.restrictions
                                    if word.word[restriction[1]] == restriction[0]])

        return restrictions_matched

    """
    Return a list of possible moves from the current node (Words which are not in the path yet)
    The current node is always a Gap
    """
    def nextMoves(self):
        # return a list containing Words that are not yet in the path
        return [word for word in self.words if word not in [pair[1] for pair in self.path]]

    def fitness(self):
        correct = 0

        for pair in self.path:
            for restrictions in pair[0].restrictions:
                if pair[1][restrictions[1]] == restrictions[0]:
                    correct += 1

        return correct
