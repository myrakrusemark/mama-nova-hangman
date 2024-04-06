# Hangman Game

This is a two-player Hangman game created in Python using the Tkinter library for the graphical user interface (GUI). The game was developed in a morning session with my daughter after enjoying the paper version of the game. We collaborated with Anthropic's Claude3 to write the entire program, including the GUI and game logic, in about 3 hours. The background image for the game was generated using DallE 3.

## Rules of the Game

1. The game is played between two players, taking turns as the "word provider" and the "guesser."
2. The word provider enters a word or phrase, and the guesser tries to guess it by suggesting letters.
3. The guesser has a limited number of chances (8) to guess the word correctly.
4. If the guesser suggests a correct letter, it is revealed in the word. If the guess is incorrect, they lose a chance.
5. The guesser can also guess the entire word at once, but an incorrect word guess counts as a lost chance.
6. The word provider can give a hint to the guesser, but it will cost them points.
7. The game ends when the guesser either guesses the word correctly or runs out of chances.
8. The players switch roles after each round.

## Scoring Mechanisms

- Word Provider:
  - Receives 2 points for winning the round (guesser runs out of chances)
  - Receives 5 points if the guesser uses a hint

- Guesser:
  - Receives 2 points for each correct letter guess
  - Receives 2 points for each remaining letter in the word if they guess the entire word correctly

## Requirements

- Python 3.x
- Tkinter library
- PIL (Python Imaging Library)

## How to Run

1. Make sure you have Python 3.x installed on your system.
2. Install the required libraries by running the following command:
   ```
   pip install tkinter pillow
   ```
3. Save the provided code in a Python file (e.g., `hangman.py`).
4. Place the background image file (`bg.png`) in the same directory as the Python file.
5. Run the Python file using the following command:
   ```
   python hangman.py
   ```

## Acknowledgements

- The game was developed using Anthropic's Claude3 AI assistant.
- The background image was generated using DallE 3.

Enjoy playing Hangman with your friends and family!