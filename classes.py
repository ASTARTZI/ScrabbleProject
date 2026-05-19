import random
import unicodedata
import itertools


def documentation():
    """
    - Κλάσεις: Player, Human, Computer, SakClass, Game.
    - Κληρονομικότητα: Οι Human και Computer κληρονομούν από την Player.
    - Επέκταση μεθόδων: Η μέθοδος play() ορίζεται στην Player και επεκτείνεται στις Human και Computer.
    - Δομή λέξεων: Οι λέξεις αποθηκεύονται σε set για αναζήτηση O(1).
    - Αλγόριθμος πολιτικής παιχνιδιού: Min-Max-Smart.
    - Πρότυπο Mediator: Η Game συντονίζει την επικοινωνία μεταξύ Human, Computer και SakClass.
    """
    pass


def normalize_word(word):
    word = word.strip().upper()
    word = word.replace("Σ", "Σ")

    normalized = unicodedata.normalize("NFD", word)
    without_accents = ""

    for char in normalized:
        if unicodedata.category(char) != "Mn":
            without_accents += char

    return without_accents


class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.letters = []

    def __repr__(self):
        return f"Παίκτης: {self.name}, Σκορ: {self.score}, Γράμματα: {self.letters}"

    def play(self, game):
        raise NotImplementedError


class Human(Player):

    def __init__(self, name):
        super().__init__(name)

    def play(self, game):

        print("\n-----------------------------------")
        print(f"Παίκτης: {self.name}")
        print(f"Σκορ: {self.score}")
        print("Γράμματα:", self.letters)

        word = normalize_word(input("\nΔώσε λέξη: "))

        if word == "Q":
            game.running = False
            return

        if word == "P":
            game.sak.putbackletters(self.letters)
            self.letters = game.sak.getletters(7)
            print("Έγινε αλλαγή γραμμάτων.")
            return

        if not game.is_valid_word(word):
            print("Μη αποδεκτή λέξη.")
            return

        if not game.can_form_word(word, self.letters):
            print("Η λέξη υπάρχει, αλλά δεν μπορείς να τη σχηματίσεις με τα γράμματά σου.")
            return

        points = game.calculate_word_score(word)
        self.score += points

        print(f"Αποδεκτή λέξη! Πόντοι: {points}")

        for letter in word:
            self.letters.remove(letter)

        self.letters.extend(game.sak.getletters(7 - len(self.letters)))


class Computer(Player):

    import itertools


class Computer(Player):

    def __init__(self, name="Computer", strategy="SMART"):

        super().__init__(name)

        self.strategy = strategy

    def play(self, game):

        print("\n-----------------------------------")
        print(f"Σειρά υπολογιστή ({self.strategy})...")

        possible_words = []

        # MIN STRATEGY
        if self.strategy == "MIN":

            for length in range(2, 8):

                for permutation in itertools.permutations(self.letters, length):

                    word = "".join(permutation)

                    if game.is_valid_word(word):

                        self.play_word(game, word)
                        return

        # MAX STRATEGY
        elif self.strategy == "MAX":

            for length in range(7, 1, -1):

                for permutation in itertools.permutations(self.letters, length):

                    word = "".join(permutation)

                    if game.is_valid_word(word):

                        self.play_word(game, word)
                        return

        # SMART STRATEGY
        elif self.strategy == "SMART":

            for length in range(2, 8):

                for permutation in itertools.permutations(self.letters, length):

                    word = "".join(permutation)

                    if game.is_valid_word(word):

                        if word not in possible_words:

                            possible_words.append(word)

            if possible_words:

                best_word = max(
                    possible_words,
                    key=lambda w: game.calculate_word_score(w)
                )

                self.play_word(game, best_word)
                return

        print("Ο υπολογιστής δεν βρήκε λέξη.")

        game.sak.putbackletters(self.letters)

        self.letters = game.sak.getletters(7)

    def play_word(self, game, word):

        points = game.calculate_word_score(word)

        self.score += points

        print(f"Ο υπολογιστής έπαιξε: {word}")
        print(f"Πόντοι: {points}")

        for letter in word:

            self.letters.remove(letter)

        new_letters = game.sak.getletters(7 - len(self.letters))

        self.letters.extend(new_letters)


class SakClass:

    LETTERS = {
        "Α": [12, 1],
        "Β": [1, 8],
        "Γ": [2, 4],
        "Δ": [2, 4],
        "Ε": [8, 1],
        "Ζ": [1, 10],
        "Η": [7, 1],
        "Θ": [1, 10],
        "Ι": [8, 1],
        "Κ": [4, 2],
        "Λ": [3, 3],
        "Μ": [3, 3],
        "Ν": [6, 1],
        "Ξ": [1, 10],
        "Ο": [9, 1],
        "Π": [4, 2],
        "Ρ": [5, 2],
        "Σ": [7, 1],
        "Τ": [8, 1],
        "Υ": [4, 2],
        "Φ": [1, 8],
        "Χ": [1, 8],
        "Ψ": [1, 10],
        "Ω": [3, 3]
    }

    def __init__(self):
        self.sak = []
        self.randomize_sak()

    def randomize_sak(self):
        for letter, values in self.LETTERS.items():
            amount = values[0]
            for _ in range(amount):
                self.sak.append(letter)

        random.shuffle(self.sak)

    def getletters(self, number):
        letters_to_give = []

        for _ in range(min(number, len(self.sak))):
            letters_to_give.append(self.sak.pop())

        return letters_to_give

    def putbackletters(self, letters):
        self.sak.extend(letters)
        random.shuffle(self.sak)

    def remaining_letters(self):
        return len(self.sak)


class Game:

    def __init__(self):
        self.sak = SakClass()
        self.human = Human("Player")
        self.computer = Computer(strategy="SMART")
        self.words = set()
        self.running = True
        self.load_words()

    def __repr__(self):
        return "Scrabble Game"

    def load_words(self):
        with open("greek7.txt", encoding="utf-8") as file:
            self.words = set()

            for word in file:
                clean_word = normalize_word(word)

                if 2 <= len(clean_word) <= 7:
                    self.words.add(clean_word)

        print(f"Φορτώθηκαν {len(self.words)} λέξεις.")

    def is_valid_word(self, word):
        return word in self.words

    def can_form_word(self, word, available_letters):
        temp_letters = available_letters.copy()

        for letter in word:
            if letter in temp_letters:
                temp_letters.remove(letter)
            else:
                return False

        return True

    def calculate_word_score(self, word):
        score = 0

        for letter in word:
            score += self.sak.LETTERS[letter][1]

        return score

    def setup(self):
        print("***** SCRABBLE *****")
        self.human.letters = self.sak.getletters(7)
        self.computer.letters = self.sak.getletters(7)

    def run(self):
        while self.running:

            if self.sak.remaining_letters() == 0:
                break

            self.human.play(self)

            if not self.running:
                break

            self.computer.play(self)

            print("\n===================================")
            print("ΣΚΟΡ")
            print(f"Player: {self.human.score}")
            print(f"Computer: {self.computer.score}")
            print("===================================")

    def end(self):
        print("\n========== ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ ==========")
        print(f"Player score: {self.human.score}")
        print(f"Computer score: {self.computer.score}")

        if self.human.score > self.computer.score:
            print("Νικητής: Player")
        elif self.computer.score > self.human.score:
            print("Νικητής: Computer")
        else:
            print("Ισοπαλία")