import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox

class HangmanGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Game")
        self.geometry("600x450")

        # Load the background image
        self.bg_image = Image.open("bg.png")
        self.bg_photo = None  # Initialize bg_photo attribute

        # Create a canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Scale the background image to fit the window
        self.scale_background_image()

        self.player1_name = ""
        self.player2_name = ""

        self.score_label = ttk.Label(self, text="Welcome to Hangman!", font=("Courier", 12, "bold"), background="#e6f6fc")
        self.score_label.pack(side=tk.TOP, pady=5)
        self.canvas.create_window(300, 20, window=self.score_label)

        self.hangman_label = ttk.Label(self, text="", font=("Courier", 12), background="#e6f6fc")
        self.hangman_label.pack(pady=10)
        self.canvas.create_window(300, 200, window=self.hangman_label)

        self.input_frame = ttk.Frame(self)
        self.input_frame.pack(fill=tk.X, padx=10, pady=5)
        self.canvas.create_window(300, 400, window=self.input_frame)

        self.input_field = ttk.Entry(self.input_frame, font=("Courier", 12))
        self.input_field.pack(side=tk.LEFT, expand=True, fill=tk.X)
        self.input_field.bind("<Return>", self.submit_guess)
        self.input_field.focus_set()  # Place the cursor in the input field

        self.submit_button = ttk.Button(self.input_frame, text="Submit", command=self.submit_guess)
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.rules_button = ttk.Button(self.input_frame, text="Rules", command=self.show_rules)
        self.rules_button.pack(side=tk.LEFT, padx=5)

        self.word = ""
        self.hint = ""
        self.word_completion = ""
        self.guessed = False
        self.guessed_letters = []
        self.guessed_words = []
        self.wrong_letters = []
        self.chances = 8
        self.guesser_score = 0
        self.opponent_score = 0
        self.current_player = 1
        self.player1_score = 0
        self.player2_score = 0

        self.ask_player_names()

        # Bind the window resize event to scale the background image
        self.bind("<Configure>", self.on_resize)

    def show_rules(self):
        rules = """Rules of Hangman:
1. Opponent enters a word or phrase, and Guesser tries to guess it by suggesting letters.
2. Guesser has a limited number of chances to guess the word correctly.
3. If Guesser guesses a correct letter, it is revealed in the word. If the guess is incorrect, they lose a chance.
4. Guesser can also guess the entire word at once, but an incorrect word guess counts as a lost chance.
5. The game ends when Guesser either guesses the word correctly or runs out of chances.
6. The players switch roles after each round.

Scoring Mechanisms:
- Opponent (word provider) gets:
    - 2 points for winning the round (Guesser runs out of chances)
    - 5 points if Guesser uses a hint
- Guesser gets:
    - 2 points for each correct letter guess
    - 2 points for each remaining letter in the word if they guess the entire word correctly
        """
        messagebox.showinfo("Rules", rules)

    def scale_background_image(self):
        # Get the window dimensions
        window_width = self.canvas.winfo_width()
        window_height = self.canvas.winfo_height()

        # Resize the background image to fit the window
        resized_image = self.bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)

        # Update the background image on the canvas
        self.canvas.delete("bg_image")
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor=tk.NW, tags="bg_image")

    def on_resize(self, event):
        # Scale the background image when the window is resized
        self.scale_background_image()

    def clear_screen(self):
        self.hangman_label.config(text="")

    def ask_player_names(self):
        self.clear_screen()
        self.hangman_label.config(text=self.hangman_label.cget("text") + "Enter the name for Player 1 below. ")
        self.input_field.focus()
        self.input_field.bind("<Return>", self.submit_player1_name)
        self.submit_button.configure(command=self.submit_player1_name)

    def submit_player1_name(self, event=None):
        self.player1_name = self.input_field.get().strip()
        self.input_field.delete(0, tk.END)
        self.clear_screen()
        self.hangman_label.config(text=self.hangman_label.cget("text") + "Enter the name for Player 2 below. ")
        self.input_field.focus()
        self.input_field.bind("<Return>", self.submit_player2_name)
        self.submit_button.configure(command=self.submit_player2_name)

    def submit_player2_name(self, event=None):
        self.player2_name = self.input_field.get().strip()
        self.input_field.delete(0, tk.END)
        self.display_score()
        self.start_game()

    def display_score(self):
        score_text = f"{self.player1_name}: {self.player1_score}  |  {self.player2_name}: {self.player2_score}"
        if self.score_label is None:
            self.score_label = ttk.Label(self, text=score_text, font=("Courier", 12, "bold"))
            self.score_label.pack(side=tk.TOP, pady=5)
        else:
            self.score_label.config(text=score_text, font=("Courier", 12, "bold"))

    def display_hangman(self, chances, prepend = ""):
        stages = [  
                # final state: head, torso, both arms, both legs, eyes/frown
                    '''
                    --------
                    |      |
                    |      \U0001F641
                    |     \\|/
                    |      |
                    |     / \\
                    -
                    ''',
                    #head, chest, torso, both arms, both legs
                    '''
                    --------
                    |      |
                    |      O
                    |     \\|/
                    |      |
                    |     / \\
                    -
                    ''',
                    # head, torso, both arms, both legs
                    '''
                    --------
                    |      |
                    |      O
                    |     \\|/
                    |      |
                    |     / 
                    -
                    ''',
                    # head, torso, both arms, one leg
                    '''
                    --------
                    |      |
                    |      O
                    |     \\|/
                    |      |
                    |      
                    -
                    ''',
                    # head, torso, both arms
                    '''
                    --------
                    |      |
                    |      O
                    |     \\|/
                    |      
                    |     
                    -
                    ''',
                    # head, torso, one arm
                    '''
                    --------
                    |      |
                    |      O
                    |     \\|
                    |      
                    |     
                    -
                    ''',
                    # head, torso
                    '''
                    --------
                    |      |
                    |      O
                    |      |
                    |      
                    |     
                    -
                    ''',
                    # head
                    '''
                    --------
                    |      |
                    |      O
                    |    
                    |      
                    |     
                    -
                    ''',
                    # initial empty state
                    '''
                    --------
                    |      |
                    |      
                    |    
                    |      
                    |     
                    -
                    '''
        ]

        hangman_text = stages[chances]
        self.hangman_label.config(text=prepend+hangman_text)

    def start_game(self):
        self.clear_screen()
        self.hangman_label.config(text=self.hangman_label.cget("text") + "Let's play Hangman!\n\n")
        
        current_player_name = self.player1_name if self.current_player == 1 else self.player2_name
        self.hangman_label.config(text=self.hangman_label.cget("text") + f"{current_player_name}, enter a word or phrase below. ")
        
        self.input_field.focus()
        self.input_field.bind("<Return>", self.submit_word)
        self.submit_button.configure(command=self.submit_word)
        self.word = ""
        self.hint = ""
        self.wait_for_input()

    def wait_for_input(self):
        if not self.word:
            self.after(100, self.wait_for_input)

    def submit_word(self, event=None):
        if not self.word:
            self.word = self.input_field.get().strip().upper()
            self.input_field.delete(0, tk.END)
            self.clear_screen()
            self.hangman_label.config(text=self.hangman_label.cget("text") + "Enter a hint for \""+self.word+"\" below. ")
            self.input_field.focus()
        elif not self.hint:
            self.hint = self.input_field.get().strip()
            self.input_field.delete(0, tk.END)
            self.clear_screen()
            self.word_completion = "".join(["_" if char != " " else " " for char in self.word])
            self.guessed = False
            self.guessed_letters = []
            self.guessed_words = []
            self.wrong_letters = []
            self.chances = 7
            self.guesser_score = 0
            self.opponent_score = 0
            self.input_field.bind("<Return>", self.submit_guess)  # Rebind <Return> to submit_guess
            self.submit_button.configure(command=self.submit_guess)  # Reconfigure submit_button
            self.clear_screen()
            self.display_game()

    def display_game(self, prepend=""):
        self.clear_screen()
        self.display_score()
        self.hangman_label.config(text=self.hangman_label.cget("text") + "Let's play Hangman!\n\n")
        self.display_hangman(self.chances, prepend)  # Display the hangman using the label
        
        # Add spaces between each character of word_completion and replace spaces with three spaces
        spaced_word_completion = " ".join(["   " if char == " " else char for char in self.word_completion])
        self.hangman_label.config(text=self.hangman_label.cget("text") + spaced_word_completion + "\n\n")
        
        self.hangman_label.config(text=self.hangman_label.cget("text") + "Wrong letters: " + ", ".join(self.wrong_letters) + "\n\n")
        self.hangman_label.config(text=self.hangman_label.cget("text") + "Type 'HINT' to get a hint.\n")

    def submit_guess(self, event=None):
        guess = self.input_field.get().strip().upper()
        self.input_field.delete(0, tk.END)
        self.process_guess(guess)
        self.display_score()

    def submit_guess(self, event=None):
        guess = self.input_field.get().strip().upper()
        self.input_field.delete(0, tk.END)
        self.process_guess(guess)
        self.display_score()

    def process_guess(self, guess):
        self.clear_screen()
        prepend = ""
        if len(guess) == 1 and guess.isalpha():
            if guess in self.guessed_letters:
                prepend = "You already guessed the letter " + guess + "\n"
            elif guess not in self.word:
                prepend = guess + " is not in the word.\n"
                self.chances -= 1
                self.guessed_letters.append(guess)
                self.wrong_letters.append(guess)
                
                # If the current player is Player 1 (word provider)
                if self.current_player == 1:
                    self.player1_score += 2  # Add 2 poins to Player 1 (guesser) for an incorrect guess
                else:
                    self.player2_score += 2  # Add 2 points to Player 2 (guesser) for an incorrect guess
            else:
                prepend = "Good job, " + guess + " is in the word!\n"
                self.guessed_letters.append(guess)
                word_as_list = list(self.word_completion)
                indices = [i for i, letter in enumerate(self.word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                self.word_completion = "".join(word_as_list)
                if "_" not in self.word_completion:
                    self.guessed = True
                
                # If the current player is Player 1 (word provider)
                if self.current_player == 1:
                    self.player2_score += 2  # Add 2 points to Player 2 (guesser) for a correct letter guess
                else:
                    self.player1_score += 2  # Add 2 points to Player 1 (guesser) for a correct letter guess
        elif guess == "HINT":
            prepend = "Hint: " + self.hint + "\n"
            # If the current player is Player 1 (word provider)
            if self.current_player == 1:
                self.player1_score += 5  # Add 5 points to Player 1 (word provider) for using a hint
            else:
                self.player2_score += 5  # Add 5 points to Player 2 (word provider) for using a hint
        elif len(guess) == len(self.word) and guess.isalpha():
            if guess in self.guessed_words:
                prepend = "You already guessed the word " + guess + "\n"
            elif guess != self.word:
                prepend = guess + " is not the word.\n"
                self.chances -= 1
                self.guessed_words.append(guess)
            else:
                self.guessed = True
                self.word_completion = self.word
                remaining_letters = len(self.word) - len(self.guessed_letters)
                
                # If the current player is Player 1 (word provider)
                if self.current_player == 1:
                    # Add 2 points to Player 2 (guesser) for every remaining letter in the word
                    self.player2_score += 2 * remaining_letters
                else:
                    # Add 2 points to Player 1 (guesser) for every remaining letter in the word
                    self.player1_score += 2 * remaining_letters

            

        else:
            prepend = "Not a valid guess.\n"

        self.display_game(prepend)

        if self.guessed or self.chances == 0:
            if self.guessed:
                self.hangman_label.config(text=self.hangman_label.cget("text") + "Congratulations! You guessed the word!\n")
            else:
                self.hangman_label.config(text=self.hangman_label.cget("text") + "Sorry, you ran out of chances. The word was " + self.word + "\n")
                
                # If the current player is Player 1 (word provider)
                if self.current_player == 1:
                    self.player1_score += 2  # Add 2 points to Player 1 (word provider) for winning the round
                else:
                    self.player2_score += 2  # Add 2 points to Player 2 (word provider) for winning the round

            self.hangman_label.config(text=self.hangman_label.cget("text") + "Player 1 score: " + str(self.player1_score) + "\n")
            self.hangman_label.config(text=self.hangman_label.cget("text") + "Player 2 score: " + str(self.player2_score) + "\n\n")

            self.hangman_label.config(text=self.hangman_label.cget("text") + "Press Enter to continue...")
            self.input_field.bind("<Return>", self.continue_game)
            self.submit_button.configure(command=self.continue_game)
            self.input_field.focus()

    def continue_game(self, event=None):
        self.current_player = 2 if self.current_player == 1 else 1
        current_player_name = self.player1_name if self.current_player == 1 else self.player2_name
        self.hangman_label.config(text=self.hangman_label.cget("text") + f"\n{current_player_name}'s turn.\n\n")
        self.start_game()

if __name__ == "__main__":
    game = HangmanGame()
    game.mainloop()