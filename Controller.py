class Controller:
    def __init__(self):
        # list of ants
        self.__population = []
        # matrix
        self.__trace = [[]]

        # run parameters
        self.alpha = 0
        self.beta = 0
        self.noAnts = 0
        # iterations per epoch
        self.noIterations = 0
        # the number of times the simulation is restarteds
        self.noEpochs = 0

    def iteration(self):
        pass

    """
    @returns solution
    """
    def runAlgo(self):
        for epoch in range(self.noEpochs):
            for iteration in range(self.noIterations):
                pass

    """
    Run parameters are read from file
    """
    def loadParameters(self, filename):
        f = open(filename, "r")

        self.alpha = int(f.readline().split("=")[1])

        self.beta = int(f.readline().split("=")[1])

        self.noAnts = int(f.readline().split("=")[1])

        self.noEpochs = int(f.readline().split("=")[1])

        self.noIterations = int(f.readline().split("=")[1])

        f.close()
