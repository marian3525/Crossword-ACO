class Word:
    def __init__(self, word_str, id):
        self.id = id
        self.word = word_str

    def __str__(self):
        return "word: " + self.word + ", id:" + str(self.id)
