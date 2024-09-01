class Level2Beginner:
    def __init__(self, name, difficulty, id):
        self.name = name
        self.difficulty = difficulty
        self.id = id
        self.enemies = []
        print(self.name, self.difficulty, self.id)