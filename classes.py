# -*- coding: utf-8 -*-
import random
import itertools


def documentation():
    """
    1. Classes:
       - Game: manages the overall game (mediator).
       - SakClass: manages the bag of letters (get, put back).
       - Player: base player class.
       - Human: subclass of Player for the human.
       - Computer: subclass of Player for the computer.

    2. Inheritance:
       - Player is the base class.
       - Human(Player), Computer(Player) are subclasses.

    3. Method extension:
       - The method play() is extended differently in Human and Computer.

    4. Operator overloading / decorators:
       - __repr__ implemented in Player (string representation).
       - No decorators were used.

    5. Word structure:
       - A set is used to store and check valid words.
       - Complexity O(1) for word validation.

    6. Computer strategies:
       - MIN: plays the first acceptable word from the smallest permutations.
       - MAX: plays the first acceptable word from the largest permutations.
       - SMART: finds the permutation with the highest score.
       - FAIL: plays not always the best, sometimes 2nd or 3rd best.
       - LEARN: learns new words from the human and adds them to the dictionary.
       - TEACH: suggests the best possible word to the human.

    7. Mediator pattern:
       - The Game class works as a mediator, coordinating Human, Computer, and SakClass:
         • Distributes letters from the bag.
         • Manages moves and score.
         • Controls the flow of the game (main_menu, setup, run, end).

    8. Files:
       - classes.py: contains classes and documentation().
       - main.py: contains the main program to start the game.
       - greek7.txt: dictionary file with Greek words (loaded into a set).
    """


# ---------------- Bag -----------------
class SakClass:
    def __init__(self):
        # Greek Scrabble letters with counts and scores
        self.letters = {
            'Α': (12, 1), 'Β': (1, 8), 'Γ': (2, 4),
            'Δ': (2, 4), 'Ε': (8, 1), 'Ζ': (1, 10),
            'Η': (7, 1), 'Θ': (1, 10), 'Ι': (8, 1),
            'Κ': (4, 2), 'Λ': (3, 3), 'Μ': (3, 3),
            'Ν': (6, 1), 'Ξ': (1, 10), 'Ο': (9, 1),
            'Π': (4, 2), 'Ρ': (5, 2), 'Σ': (7, 1),
            'Τ': (8, 1), 'Υ': (4, 2), 'Φ': (1, 8),
            'Χ': (1, 8), 'Ψ': (1, 10), 'Ω': (3, 3),
        }
        self.sak = []
        self.randomize_sak()

    def randomize_sak(self):
        # Prepare and shuffle the bag with all letters
        self.sak = []
        for letter, (count, _) in self.letters.items():
            self.sak.extend([letter] * count)
        random.shuffle(self.sak)

    def getletters(self, n=7):
        # Give n letters from the bag
        hand = []
        for _ in range(min(n, len(self.sak))):
            hand.append(self.sak.pop())
        return hand

    def putbackletters(self, letters):
        # Put letters back into the bag
        self.sak.extend(letters)
        random.shuffle(self.sak)


# ---------------- Players -----------------
class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.score = 0

    def __repr__(self):
        return f"{self.name}: {''.join(self.hand)} (score: {self.score})"

    def play(self, wordset):
        raise NotImplementedError("The method must be implemented by Human or Computer")


class Human(Player):
    def play(self, wordset):
        word = input(f"{self.name}, nter a word (in Greek), or P to change letters, or Q to quit: ").strip().upper()
        return word


# ---------------- Computer -----------------
class Computer(Player):
    def __init__(self, name, strategy="SMART"):
        super().__init__(name)
        self.strategy = strategy  # MIN, MAX, SMART, FAIL, LEARN, TEACH
        self.learned_words = set()  # για Smart-Learn

    def __repr__(self):
        return f"{self.name} [Computer-{self.strategy}]: {''.join(self.hand)} (score: {self.score})"

    def play(self, wordset):
        #  Combine dictionary with learned words
        all_words = wordset | self.learned_words
        if self.strategy in ("MIN", "MAX", "SMART"):
            return self.min_max_smart(all_words)
        elif self.strategy == "FAIL":
            return self.fail_strategy(all_words)
        elif self.strategy == "LEARN":
            return self.smart_learn(all_words)
        elif self.strategy == "TEACH":
            return self.smart_teach(all_words)
        else:
            return "PASS"

    # Min-Max-Smart
    def min_max_smart(self, wordset):
        words = []
        for i in (range(2, len(self.hand) + 1) if self.strategy == "MIN" else range(len(self.hand), 1, -1)):
            for perm in itertools.permutations(self.hand, i):
                w = "".join(perm)
                if w in wordset:
                    words.append(w)
            if self.strategy in ("MIN", "MAX") and words:
                return words[0]
        # SMART: εξαντλεί όλες τις μεταθέσεις
        if self.strategy == "SMART":
            best_word = ""
            best_score = 0
            for i in range(2, len(self.hand) + 1):
                for perm in itertools.permutations(self.hand, i):
                    w = "".join(perm)
                    if w in wordset:
                        score = sum(SakClass().letters[l][1] for l in w)
                        if score > best_score:
                            best_score = score
                            best_word = w
            return best_word if best_word else "PASS"
        return "PASS"

    # Fail Strategy
    def fail_strategy(self, wordset):
        words_scores = []
        for i in range(2, len(self.hand) + 1):
            for perm in itertools.permutations(self.hand, i):
                w = "".join(perm)
                if w in wordset:
                    score = sum(SakClass().letters[l][1] for l in w)
                    words_scores.append((score, w))
        words_scores.sort(reverse=True)
        if not words_scores:
            return "PASS"
        return words_scores[1][1] if len(words_scores) > 1 else words_scores[0][1]

    # Learn Strategy
    def smart_learn(self, wordset):
        word = self.min_max_smart(wordset)
        return word

    # Teach Strategy
    def smart_teach(self, wordset):
        best_word = ""
        best_score = 0
        for i in range(2, len(self.hand) + 1):
            for perm in itertools.permutations(self.hand, i):
                w = "".join(perm)
                if w in wordset:
                    score = sum(SakClass().letters[l][1] for l in w)
                    if score > best_score:
                        best_score = score
                        best_word = w
        return best_word if best_word else "PASS"


# ---------------- Game -----------------
class Game:
    def __init__(self, wordset):
        self.sak = SakClass()
        self.wordset = wordset
        self.players = []
        self.strategy = "SMART"  # default stategy

    def __repr__(self):
        players_info = " | ".join(str(p) for p in self.players) if self.players else "No players yet"
        return f"<Game strategy={self.strategy}, players=[{players_info}], letters_left={len(self.sak.sak)}>"

    # Main Menu
    def main_menu(self):
        while True:
            print("\n**** SCRABBLE ****")
            print("------------------------------")
            print("1: Score")
            print("2: Settings")
            print("3: Play")
            print("q: Quit")
            choice = input("Choose an option: ").strip().lower()

            if choice == "1":
                self.show_scores()
            elif choice == "2":
                self.settings()
            elif choice == "3":
                self.setup()
                self.run()
                self.end()
            elif choice == "q":
                print("Exiting the game.")
                break
            else:
                print("Ivalid option!")

    # Εμφάνιση Σκορ
    def show_scores(self):
        if not self.players:
            print("No scores yet. Start the game first!")
            return
        print("\nCurrent Scores:")
        for p in self.players:
            print(p)

    # Choose Computer strategy
    def settings(self):
        print("\nΕ # Choose Computer strategy:")
        print("a: MIN (plays shortest words first)")
        print("b: MAX (plays longest words first)")
        print("c: SMART (plays the highest scoring word)")
        print("d: FAIL (sometimes plays a worse word)")
        print("e: LEARN (learns new words from human)")
        print("f: TEACH (suggests the best word to human)")

        choice = input("Choose strategy (a-f): ").strip().lower()
        strategies = {
            "a": "MIN",
            "b": "MAX",
            "c": "SMART",
            "d": "FAIL",
            "e": "LEARN",
            "f": "TEACH",
        }
        self.strategy = strategies.get(choice, "SMART")
        print(f"Strategy selected: {self.strategy}")

    # Setup players
    def setup(self):
        self.players = [
            Human("HUMAN"),
            Computer("COMPUTER", strategy=self.strategy)
        ]
        for p in self.players:
            p.hand = self.sak.getletters(7)

    # Run the game
    def run(self):
        turn = 0
        while True:
            player = self.players[turn % 2]
            print(player)
            word = player.play(self.wordset)

            if word == "Q":
                print(f"{player.name} quit the game!")
                break
            elif word == "P":
                self.sak.putbackletters(player.hand)
                player.hand = self.sak.getletters(7)
                print("Letters changed!")
            elif word in self.wordset and all(word.count(l) <= player.hand.count(l) for l in word):
                score = sum(self.sak.letters[l][1] for l in word)
                player.score += score
                for l in word:
                    player.hand.remove(l)
                player.hand.extend(self.sak.getletters(7 - len(player.hand)))
                print(f"{player.name} played {word} (+{score})")
            elif word == "PASS":
                print(f"{player.name} could not find a word and passed.")
            elif isinstance(player, Human) and self.strategy == "TEACH":
                computer = next(p for p in self.players if isinstance(p, Computer))
                best_word = computer.smart_teach(self.wordset)
                if word in self.wordset:
                    print(f"(ΥΠΟΛΟΓΙΣΤΗΣ-TEACH) The best word would have been: {best_word}")
            else:
                print("Invalid word!!")

            if not self.sak.sak:
                print("No more letters left in the bag.")
                break
            turn += 1

    # End of game
    def end(self):
        print("\nGame Over!")
        for p in self.players:
            print(p)

        # Save new words if LEARN strategy was used
        for p in self.players:
            if isinstance(p, Computer) and p.strategy == "LEARN" and p.learned_words:
                with open("greek7.txt", "a", encoding="utf-8") as f:
                    for w in p.learned_words:
                        f.write(w + "\n")
                print(f"New words saved to greek7.txt: {len(p.learned_words)} words.")

