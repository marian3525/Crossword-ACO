from Problem import Problem
from Ant import Ant
from copy import deepcopy
from Word import Word

class Controller:
    def __init__(self):
        # list of ants
        self.__population = []

        # run parameters
        self.alpha = 0
        self.beta = 0
        self.noAnts = 0
        self.evaporationCoef = 0

        self.ants = []
        # iterations per epoch
        self.noIterations = 0
        # the number of times the simulation is restarted
        self.noEpochs = 0

        self.q0 = 0
        # load the problem data
        self.problem = Problem()

        # matrix, global trace,
        # matrix(i, j) = the pheromone trace value from the gap with id 'i' to the word with id 'j'
        self.trace = [[0 for _ in range(self.problem.nblanks)] for _ in range(self.problem.nblanks)]

        self.loadParameters("param.in")

    '''
    Return the matching found by the best ant as a list of (gap, word)
    '''
    def iteration(self):
        # create and give the ants their starting node
        self.ants.clear()

        words = []
        counter = 0
        for word_str in self.problem.words_str:
            words.append(Word(word_str, counter))
            counter += 1

        for i in range(self.noAnts):
            # startGap = self.problem.gaps[0] # should be random?
            ant = Ant(self.problem.gaps, words, self.trace, self.alpha, self.beta, self.q0)
            self.ants.append(deepcopy(ant))

        # update the ants
        for step in range(self.noIterations):
            # update each ant
            for ant in self.ants:
                ant.update()

        # leave a trace in the matrix for the best ant
        newTrace = [ant.fitness() for ant in self.ants]

        for i in range(self.problem.nblanks):
            for j in range(self.problem.nblanks):
                self.trace[i][j] = (1-self.evaporationCoef) * self.trace[i][j]

        for i in range(self.noAnts):
            for j in range(len(self.ants[i].path) - 1):
                # create a new edge from the n-1 th node to the last node added, todo? what is the last node
                # todo, what is x and y, for gaps or words?
                x = self.ants[i].path[j][0].id
                y = self.ants[i].path[j-1][0].id
                self.trace[x][y] = self.trace[x][y] + newTrace[i]

        # return the path of the best ant
        fitneses = [(self.ants[i].fitness(), i) for i in range(self.noAnts)]
        maxFit = max(fitneses, key=lambda e: e[0])
        return self.ants[maxFit[1]].path

    """
    @returns solution
    """
    def runAlgo(self):
        for epoch in range(self.noEpochs):
            current_solution = self.iteration()
            print("Solution:")
            for pair in current_solution:
                print(str(pair[0]), "\n", str(pair[1]))

    """
    Run parameters are read from file
    """
    def loadParameters(self, filename):
        f = open(filename, "r")

        self.alpha = float(f.readline().split("=")[1])

        self.beta = float(f.readline().split("=")[1])

        self.noAnts = int(f.readline().split("=")[1])

        self.noEpochs = int(f.readline().split("=")[1])

        self.noIterations = int(f.readline().split("=")[1])

        self.evaporationCoef = float(f.readline().split("=")[1])

        f.close()
