from Gap import Gap
from Point import Point

class Problem:
    def __init__(self):
        # problem data
        # specific data
        self.blanks = []
        self.nblanks = 0
        self.sizeX = 0
        self.sizeY = 0
        # list of (word_str, (Point(boardx_start, boardy_start), Point(boardx_end, boardy_end))
        self.gaps = []
        self.words_str = []

        self.loadProblem("data.in")
        # the restrictions are populated and checked when inserting word strings into an individual's list of words

    def loadProblem(self, filename):
        f = open(filename, "r")

        blanks = int(f.readline())
        self.sizeX = int(f.readline())
        self.sizeY = int(f.readline())
        cl = 0

        while cl < blanks:
            line = f.readline()
            line = line.split(" ")
            self.blanks.append((int(line[0]), int(line[1])))
            cl += 1

        self.nblanks = blanks

        self.words_str = f.readline().split(",")

        # build a temp matrix and count the words on vertical/horiz
        matrix = [[] for _ in range(self.sizeY)]

        for l in matrix:
            for i in range(self.sizeY):
                l.append("")

        for pair in self.blanks:
            # mark the blank tiles
            matrix[pair[0]][pair[1]] = "0"

        startedWordLine = False

        i_s_line = 0
        j_s_line = 0

        gap_id = 0

        for i in range(self.sizeY):
            for j in range(self.sizeX):
                # on lines
                if not startedWordLine and matrix[i][j] == "":
                    i_s_line = i
                    j_s_line = j
                    startedWordLine = True

                elif startedWordLine and matrix[i][j] == "0" or j == self.sizeX - 1:
                    i_e_line = i
                    j_e_line = j
                    if j_e_line - j_s_line >= 2:
                        word_str = ""
                        size = j_e_line - j_s_line + 1
                        point_start = Point(j_s_line, i_s_line)
                        point_end = Point(j_e_line, i_e_line)

                        self.gaps.append(Gap(word_str, size, point_start, point_end, gap_id))
                        gap_id += 1

                    startedWordLine = False

        startedWordLine = False

        for j in range(self.sizeX):
            for i in range(self.sizeY):
                if not startedWordLine and matrix[i][j] == "":
                    i_s_line = i
                    j_s_line = j
                    startedWordLine = True

                elif startedWordLine and matrix[i][j] == "0" or i == self.sizeY - 1:
                    i_e_line = i
                    j_e_line = j
                    if i_e_line - i_s_line >= 2:
                        word_str = ""
                        size = i_e_line - i_s_line + 1
                        point_start = Point(j_s_line, i_s_line)
                        point_end = Point(j_e_line, i_e_line)

                        self.gaps.append(Gap(word_str, size, point_start, point_end, gap_id))
                        gap_id += 1
                    startedWordLine = False

        f.close()

