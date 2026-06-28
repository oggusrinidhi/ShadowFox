"""Terminal Hangman game with visual progress and hints.

Run normally:
    python hangman.py

Show sample output:
    python hangman.py --demo
"""

from __future__ import annotations

import random
import sys
from dataclasses import dataclass


HANGMAN_STAGES = [
    """
      +---+
      |   |
          |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========
    """,
    """
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========
    """,
]


@dataclass
class WordEntry:
    word: str
    hint: str


WORDS = [
    WordEntry("python", "A popular programming language."),
    WordEntry("computer", "An electronic machine that processes data."),
    WordEntry("keyboard", "A device used to type letters and commands."),
    WordEntry("internet", "A global network that connects computers."),
    WordEntry("algorithm", "A step-by-step method to solve a problem."),
]


def display_word(secret_word: str, guessed_letters: set[str]) -> str:
    return " ".join(letter if letter in guessed_letters else "_" for letter in secret_word)


def print_game_state(
    secret_word: str,
    hint: str,
    guessed_letters: set[str],
    wrong_guesses: list[str],
    max_wrong: int,
) -> None:
    print(HANGMAN_STAGES[len(wrong_guesses)])
    print(f"Word: {display_word(secret_word, guessed_letters)}")
    print(f"Hint: {hint}")
    print(f"Wrong guesses: {', '.join(wrong_guesses) if wrong_guesses else 'None'}")
    print(f"Attempts left: {max_wrong - len(wrong_guesses)}\n")


def play_game(entry: WordEntry, demo_guesses: list[str] | None = None) -> None:
    secret_word = entry.word.lower()
    guessed_letters: set[str] = set()
    wrong_guesses: list[str] = []
    max_wrong = len(HANGMAN_STAGES) - 1
    demo_index = 0

    print("Welcome to Hangman!")
    print("Guess the hidden word one letter at a time.\n")

    while len(wrong_guesses) < max_wrong:
        print_game_state(
            secret_word,
            entry.hint,
            guessed_letters,
            wrong_guesses,
            max_wrong,
        )

        if all(letter in guessed_letters for letter in secret_word):
            print(f"You won! The word was: {secret_word}")
            return

        if demo_guesses is not None:
            if demo_index >= len(demo_guesses):
                print("Demo ended before the game finished.")
                return
            guess = demo_guesses[demo_index]
            demo_index += 1
            print(f"Your guess: {guess}")
        else:
            guess = input("Your guess: ").lower().strip()

        if len(guess) != 1 or not guess.isalpha():
            print("Please enter one alphabet letter.\n")
            continue

        if guess in guessed_letters or guess in wrong_guesses:
            print("You already guessed that letter.\n")
            continue

        if guess in secret_word:
            guessed_letters.add(guess)
            print("Correct guess!\n")
        else:
            wrong_guesses.append(guess)
            print("Wrong guess!\n")

    print_game_state(secret_word, entry.hint, guessed_letters, wrong_guesses, max_wrong)
    print(f"Game over! The word was: {secret_word}")


def main() -> None:
    if "--demo" in sys.argv:
        demo_entry = WordEntry("python", "A popular programming language.")
        play_game(demo_entry, demo_guesses=["p", "x", "y", "t", "h", "o", "n"])
        return

    play_game(random.choice(WORDS))


if __name__ == "__main__":
    main()
