
import classes

if __name__ == "__main__":
    # Load Greek words into set
    with open("greek7.txt", "r", encoding="utf-8") as f:
        wordset = set(w.strip().upper() for w in f)

    # Create game
    game = classes.Game(wordset)

    # Start game through main menu
    game.main_menu()
