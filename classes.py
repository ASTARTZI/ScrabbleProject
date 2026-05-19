import random
import unicodedata
import itertools


def documentation():
    """
    Τεκμηρίωση εργασίας Python Scrabble.

    - Κλάσεις:
      Υλοποιούνται οι κλάσεις Player, Human, Computer, SakClass και Game.
      Η Player αναπαριστά έναν γενικό παίκτη.
      Η Human αναπαριστά τον άνθρωπο-παίκτη.
      Η Computer αναπαριστά τον παίκτη-υπολογιστή.
      Η SakClass διαχειρίζεται το σακουλάκι με τα γράμματα.
      Η Game διαχειρίζεται τη συνολική ροή του παιχνιδιού.

    - Κληρονομικότητα:
      Οι κλάσεις Human και Computer κληρονομούν από την Player.
      Έτσι μοιράζονται κοινές ιδιότητες, όπως name, score και letters.

    - Επέκταση μεθόδων και πολυμορφισμός:
      Η μέθοδος play() ορίζεται στην Player και επεκτείνεται διαφορετικά
      στις κλάσεις Human και Computer.
      Στην Human η play() ζητά είσοδο από τον χρήστη.
      Στην Computer η play() επιλέγει αυτόματα λέξη με βάση τη στρατηγική.
      Με αυτόν τον τρόπο εφαρμόζεται πολυμορφισμός.

    - Υπερφόρτωση τελεστών:
      Δεν έχει υλοποιηθεί υπερφόρτωση τελεστών.

    - Decorators:
      Δεν έχουν χρησιμοποιηθεί decorators.

    - Δομή λέξεων:
      Οι λέξεις του αρχείου greek7.txt φορτώνονται σε set.
      Η επιλογή set επιτρέπει γρήγορο έλεγχο ύπαρξης λέξης με μέση
      χρονική πολυπλοκότητα O(1).

    - Αλγόριθμος πολιτικής παιχνιδιού:
      Υλοποιείται ο αλγόριθμος Min-Max-Smart.
      Στη στρατηγική MIN ο υπολογιστής ψάχνει από λέξεις 2 γραμμάτων
      προς λέξεις 7 γραμμάτων και παίζει την πρώτη αποδεκτή.
      Στη στρατηγική MAX ψάχνει από λέξεις 7 γραμμάτων προς λέξεις
      2 γραμμάτων και παίζει την πρώτη αποδεκτή.
      Στη στρατηγική SMART βρίσκει όλες τις αποδεκτές λέξεις που μπορεί
      να σχηματίσει και παίζει αυτή με τους περισσότερους πόντους.

    - Πρότυπο Mediator:
      Η κλάση Game λειτουργεί ως Mediator.
      Συντονίζει την επικοινωνία μεταξύ Human, Computer και SakClass.
      Οι παίκτες δεν διαχειρίζονται απευθείας ολόκληρο το παιχνίδι,
      αλλά χρησιμοποιούν τις μεθόδους της Game για έλεγχο λέξεων,
      υπολογισμό πόντων, μοίρασμα γραμμάτων και ροή παιχνιδιού.
    """
    pass


def normalize_word(word):

    word = word.strip().upper()

    normalized = unicodedata.normalize("NFD", word)

    return "".join(
        char for char in normalized
        if unicodedata.category(char) != "Mn"
    )


class Player:

    def __init__(self, name):

        self.name = name
        self.score = 0
        self.letters = []

    def __repr__(self):

        return f"Παίκτης: {self.name}, Σκορ: {self.score}"

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

        # QUIT
        if word == "Q":

            game.running = False
            return True

        # PASS / CHANGE LETTERS
        if word == "P":

            game.sak.putbackletters(self.letters)

            self.letters = game.sak.getletters(7)

            print("Έγινε αλλαγή γραμμάτων.")

            return True

        # INVALID WORD
        if not game.is_valid_word(word):

            print("Μη αποδεκτή λέξη.")

            return False

        # CANNOT FORM WORD
        if not game.can_form_word(word, self.letters):

            print("Δεν μπορείς να σχηματίσεις αυτή τη λέξη.")

            return False

        # VALID WORD
        points = game.calculate_word_score(word)

        self.score += points

        print(f"Αποδεκτή λέξη! Πόντοι: {points}")

        for letter in word:

            self.letters.remove(letter)

        self.letters.extend(
            game.sak.getletters(7 - len(self.letters))
        )

        return True


class Computer(Player):

    def __init__(self, name="Computer", strategy="SMART"):

        super().__init__(name)

        self.strategy = strategy

    def play(self, game):

        print("\n-----------------------------------")
        print(f"Σειρά υπολογιστή ({self.strategy})...")

        possible_words = []

        # MIN
        if self.strategy == "MIN":

            for length in range(2, 8):

                for permutation in itertools.permutations(self.letters, length):

                    word = "".join(permutation)

                    if game.is_valid_word(word):

                        self.play_word(game, word)
                        return

        # MAX
        elif self.strategy == "MAX":

            for length in range(7, 1, -1):

                for permutation in itertools.permutations(self.letters, length):

                    word = "".join(permutation)

                    if game.is_valid_word(word):

                        self.play_word(game, word)
                        return

        # SMART
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

        self.letters.extend(
            game.sak.getletters(7 - len(self.letters))
        )


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

        self.computer = Computer()

        self.words = set()

        self.running = True

        self.load_words()

    def __repr__(self):

        return "Scrabble Game"

    def menu(self):

        while True:

            print("\n========== SCRABBLE ==========")
            print("1. Παιχνίδι")
            print("2. Ρυθμίσεις")
            print("3. Έξοδος")

            choice = input("\nΕπιλογή: ")

            if choice == "1":

                self.setup()

                self.run()

                self.end()

            elif choice == "2":

                self.settings()

            elif choice == "3":

                print("Έξοδος...")
                break

            else:

                print("Μη έγκυρη επιλογή.")

    def settings(self):

        print("\n========== ΡΥΘΜΙΣΕΙΣ ==========")
        print("1. MIN")
        print("2. MAX")
        print("3. SMART")

        choice = input("\nΕπιλογή στρατηγικής: ")

        if choice == "1":

            self.computer.strategy = "MIN"

        elif choice == "2":

            self.computer.strategy = "MAX"

        elif choice == "3":

            self.computer.strategy = "SMART"

        else:

            print("Μη έγκυρη επιλογή.")
            return

        print(f"\nΝέα στρατηγική: {self.computer.strategy}")

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

        self.running = True

        self.human.score = 0
        self.computer.score = 0

        self.sak = SakClass()

        self.human.letters = self.sak.getletters(7)

        self.computer.letters = self.sak.getletters(7)

        print("\n***** SCRABBLE *****")

    def run(self):

        while self.running:

            if self.sak.remaining_letters() == 0:

                break

            valid_move = self.human.play(self)

            if not self.running:

                break

            # Αν ο παίκτης έδωσε άκυρη λέξη,
            # δεν παίζει ο υπολογιστής
            if not valid_move:

                continue

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