"""
Programmed by tnelsonw for fun.
"""
from random import randint
from typing import List
from collections import Counter
from enum import Enum
import tkinter as tk

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

init_suggestions5 = ["irate", "sound", "graph", "teach", "words", "sloth", "reach", "itchy", "steal", "cheat", "meats",
                     "arise", "raise"]

init_suggestions6 = ["satire", "aspire", "mouthy", "plough", "amends", "tricky", "wavier"]

print_order = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth", 5: "sixth"}

# loosely based on commonality of each letter https://www3.nd.edu/~busiforc/handouts/cryptography/letterfrequencies.html
letter_values = {'a': 1, 'b': 3, 'c': 1, 'd': 2, 'e': 1, 'f': 4, 'g': 3, 'h': 3, 'i': 1, 'j': 10, 'k': 5, 'l': 1,
                 'm': 2, 'n': 1, 'o': 1, 'p': 2, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 2, 'v': 5, 'w': 4, 'x': 8,
                 'y': 4, 'z': 10}


class Color(Enum):
    YELLOW = ("yellow", "y")
    GREEN = ("green", "g")
    BLANK = ("blank", "b")


color_list = Color.YELLOW.value + Color.GREEN.value + Color.BLANK.value


class Wordle_Suggestor:


    def __init__(self):
        self.all_vars = list()
        # translation table built to remove default values from StringVar names
        self.translation_table = str.maketrans('', '', 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ _.!<>')
        self.gui = None
        self.frame = None
        self.counter = 0
        self.error_label = None
        self.info_label = None
        self.rand_option = None

    def set_error_label(self, message: str) -> None:
        self.error_label = tk.Label(self.frame, fg='red', text=message, width=20)
        self.error_label.grid(row=6, column=1)

    def set_info_label(self, message: str) -> None:
        self.info_label = tk.Label(self.frame, text=message, width=20)
        self.info_label.grid(row=6, column=3)

    def load_dictionary(self, number: int) -> List[str]:
        """Takes a number and loads the corresponding word dictionary, returning it as a list of strings."""
        file_name = "dictionary" + str(number) + ".txt"
        with open(file_name) as file:
            return [line.rstrip() for line in file.readlines()]


    def get_init_suggestion(self, number: int) -> str:
        """Must input integer of 5 or 6. Outputs a randomly suggested string with length of the input number"""
        if number == 5:
            return init_suggestions5[randint(0, len(init_suggestions5) - 1)]
        elif number == 6:
            return init_suggestions6[randint(0, len(init_suggestions6) - 1)]


    def check_duplicate(self, word: str) -> bool:
        """Returns true if there are duplicate letters in a word, otherwise returns false."""
        return max(Counter(word).values()) > 1


    def load_input(self, all_words: List[str], num: int) -> dict:
        """Takes all the possible words and the length of the word as input.
        Returns a dictionary with the 0-num position as the keys, and a list containing the color of the guess followed
        by the letter of the guess at that position."""
        output = {}
        word_guess: str = ""
        while True:
            for i in range(num):
                print(f'Input the {print_order[i]} letter of your guess: ')
                letter = input()
                while letter not in letter_list:
                    print("Please type a single letter followed by 'enter': ")
                    letter = input()
                letter = letter.lower()
                word_guess += letter

                print("Input the color (Yellow, Green, Blank)")
                color = input()
                while color not in color_list:
                    print("Please type either Yellow (y), Green (g), or Blank (b): ")
                    color = input()
                color = color.lower()

                output[i] = [color, letter]
            if word_guess not in all_words:
                print(f"{word_guess} is not a valid guess. Please double check your input for correctness.\n\n")
                word_guess = ""
            else:
                break
        return output


    def suggest_word(self, find: dict, confirmed: dict, remove: dict, remaining_words: List[str]) -> List[str]:
        """Reduces the amount of remaining words by eliminating words that are impossible based on the input."""
        if "" in remaining_words:
            remaining_words.remove("")

        # remove words that don't have a matching letter to the confirmed (green) positions
        for position, letter in confirmed.items():
            for word in remaining_words.copy():
                if word.find(letter, position) != position:
                    remaining_words.remove(word)

        # remove the word if the letter found (yellow) is at that same position (it should be elsewhere in the word)
        # also remove if the word does not have that letter
        for position, letter in find.items():
            for word in remaining_words.copy():
                if word.find(letter, position) == position:
                    remaining_words.remove(word)
                elif letter not in word:
                    remaining_words.remove(word)

        # remove blank letters unless if they are confirmed (green) or found (yellow) in the word
        for position, letter in remove.items():
            for word in remaining_words.copy():

                # remove the word if the letter matched the letter at the blank position
                p = word.find(letter, position, position + 1)
                if p == position:
                    remaining_words.remove(word)

                # for the rest of the word, requires more checks (could be yellow or green in other positions)
                elif p in remove.keys():
                    remaining_words.remove(word)
                elif letter in word and letter not in confirmed.values() and letter not in find.values():
                    remaining_words.remove(word)
                else:
                    # for when letters are green and blank but at a different blank position
                    for pos in [word.find(letter, x, x+1) for x in remove.keys() if word.find(letter, x, x+1) != -1]:
                        if word[pos] in remove.values() and word[pos] == remove[pos]:
                            remaining_words.remove(word)
        return remaining_words


    def find_rand_suggestion(self, suggestions: List[str]) -> str:
        """
        Simply gets a random word from the 'most likely' list of words, or words with the lowest score
        """
        return suggestions[randint(0, len(suggestions)-1)]


    # noinspection PyDefaultArgument
    def calculate_values(self, remaining_words: List[str], positions_to_check: List[int] = [], find_pos: dict = {},
                         confirmed_pos: dict = {}) -> List[str]:
        """Calculate total point values for each remaining word based on the letter_values dictionary.
        Return the list of words with the lowest calculated score, or the most likely words"""
        value_dictionary = {}
        for word in remaining_words:
            value_dictionary[word] = sum([val * letter_values[key] for key, val in Counter(word).items()])

        # skip if there are no found (yellow) letters
        if find_pos != {}:

            # cycle through each remaining word
            for word in remaining_words:

                # cycle through each letter found (yellow)
                for position, letter in find_pos.items():

                    # cycle through each position that is not confirmed (green)
                    for pos in positions_to_check:

                        p = word.find(letter, pos, pos+1)
                        # if the letter is not in a confirmed (green) space, and not in its own found (yellow) space
                        # and IS in the word
                        if p not in confirmed_pos.keys() and p != position and p != -1:
                            # subtract the value of the letter from the value_dictionary since this word is more likely
                            value_dictionary[word] -= letter_values[letter]

        # switch keys and values so that each total score has a list of valid words
        # {5: ['raise', 'arise', 'irate'], 7: ['heats', 'beats']...etc}
        v_dict = {}
        for k, v in value_dictionary.items():
            v_dict[v] = [key for key, value in value_dictionary.items() if value == v]

        # return the list with the lowest key as these are the most likely candidates
        return v_dict[min(v_dict.keys())]


    def load_gui_input(self, num_letters: int, row: int | None = None):
        """
        Load the input from the GUI
        :return: a dictionary with the 0-num position as the keys, and a list containing the color of the guess followed
        by the letter of the guess at that position.
        """
        if row is None:
            row = self.counter

        options = {}
        next: bool = False
        position: int = 0
        for k, c in enumerate(reversed(self.frame.grid_slaves(row))):

            if type(c) == tk.Entry:
                letter: str = c.get()

            elif type(c) == tk.OptionMenu:
                z: int = (int(k/2) - 1) + (row * num_letters)
                color: str = self.all_vars[z].get().lower()
                next = True

            if next:
                options[position] = [color, letter]
                position += 1
                next = False
        return options


    def process(self, all_words: List[str], num_letters: int, row: int | None = None):
        """
        This function does the main body of work for this application.
        :param all_words: All possible remaining words
        :param num_letters: The number of letters for the word
        :param row: The current row for input in the GUI
        """
        guess_output = self.load_gui_input(num_letters, row)
        find_positions = {}
        confirmed_positions = {}
        remove_positions = {}
        for key, val in guess_output.items():
            if val[0] in Color.YELLOW.value:
                find_positions[key] = val[1]
            elif val[0] in Color.GREEN.value:
                confirmed_positions[key] = val[1]
            elif val[0] in Color.BLANK.value:
                remove_positions[key] = val[1]

        # remaining positions to check are all positions not confirmed (green)
        positions_to_check = [x for x in range(num_letters) if x not in list(confirmed_positions.keys())]
        all_words = self.suggest_word(find_positions, confirmed_positions, remove_positions, all_words)
        new_suggestions = self.calculate_values(all_words, positions_to_check, find_positions, confirmed_positions)
        self.rand_option = self.find_rand_suggestion(new_suggestions)

        if self.counter < 4 and self.check_duplicate(self.rand_option):
            self.rand_option = self.find_rand_suggestion(new_suggestions)

        if self.rand_option == "":
            print("There are no suggested words available. Please double check that you input your information "
                  "correctly.")
            self.set_error_label("There are no suggested\nwords. Please double\ncheck the input.")
            exit(0)

        self.set_info_label(f"There are {len(all_words)} possible\nwords remaining.\n"
                            f"Your next suggestion is\n{self.rand_option}.")

        def new_suggestion():
            """
            This dictionary does not match with Wordle's dictionary,
            so recalculate the suggestions.
            """
            new_suggestions = self.calculate_values(all_words, positions_to_check, find_positions, confirmed_positions)
            if len(new_suggestions) == 0:
                print("There are no suggested words available. Please double check that you input your information "
                      "correctly.")
                exit(0)
            self.rand_option = self.find_rand_suggestion(new_suggestions)
            self.set_info_label(
                f"There are {len(all_words)} possible\nwords remaining.\nYour next suggestion is\n{self.rand_option}.")

        # add button for new suggestion
        suggestion_button = tk.Button(self.frame, text="New Suggestion", width=15, command=new_suggestion,
                                      background='yellow')
        suggestion_button.grid(row=6, column=5)

        def completed_wordle():
            self.info_label.after(1, self.info_label.destroy())
            self.set_info_label(f"      \nCongratulations!\nYou got the Wordle!\n     ")

        completed_button = tk.Button(self.frame, text="Got the Wordle!", width=15, command=completed_wordle,
                                     background='lightgreen')
        completed_button.grid(row=6, column=7)

        def invalid_suggestion():
            if len(all_words) > 1:
                all_words.remove(self.rand_option)
                self.set_info_label(f"Invalid word\n'{self.rand_option}'\n removed from\ndictionary.")
                self.process(all_words, num_letters, self.counter - 1)
            else:
                self.set_error_label(f"Cannot remove last\n word from dictionary.\nDouble check input.")

        # add button for word not in dictionary
        invalid_word_button = tk.Button(self.frame, text="Invalid Suggestion", width=20, command=invalid_suggestion,
                                        background='red')
        invalid_word_button.grid(row=6, column=9)


    def gui_add_row(self, row_num: int, num_letters: int) -> None:
        """
        Add all GUI elements to the window
        :param row_num: The current row to add.
        :param num_letters: The number of letters in this Wordle.
        """
        l = tk.Label(self.frame, text=f"Guess {row_num + 1}")
        l.grid(row=row_num, column=0)

        for i in range(1, num_letters*2 + 1, 2):
            e = tk.Entry(self.frame)
            e.grid(row=row_num, column=i)

            variable = tk.StringVar(self.frame)
            variable.set("Blank")  # default value
            self.all_vars.append(variable)

            w = tk.OptionMenu(self.frame, variable, "Blank", "Yellow", "Green")
            w.grid(row=row_num, column=i + 1)

            def selection_changed(var, var_num):
                """
                This function is called when a drop-down selection is changed.
                When a selection is changed, it changes the label's color to match the selection.
                :param var: The variable that changed.
                :param var_num: The number of the corresponding variable.
                """
                if var_num == 1:
                    var_num = ''  # for first entry only

                for k, c in enumerate(self.frame.grid_slaves(row_num)):
                    if type(c) == tk.Entry and str(c).translate(self.translation_table) == str(var_num):
                        match var:
                            case 'Blank':
                                color = "gray"
                            case 'Yellow':
                                color = 'yellow'
                            case 'Green':
                                color = 'lightgreen'
                            case _:
                                color = "white"
                        c.configure({'background': color})
                        break
                    #
                    # if type(c) == tk.OptionMenu and str(c).translate(self.translation_table) ==  str(var_num):
                    #     color: str = c

            def lam(*args):
                var_num: int = int(args[0].translate(self.translation_table))
                selection_changed(self.all_vars[var_num].get(), var_num + 1)

            variable.trace("w", lam)


    def main(self):
        main_window = tk.Tk()
        main_window.title("Wordle Suggestor")

        def load(num_letters: int):
            """
            Load the words and new GUI window.
            :param num_letters: The number of letters in this Wordle.
            """
            all_words: List[str] = self.load_dictionary(num_letters)
            initial_suggestion = self.get_init_suggestion(num_letters)

            # gui section
            self.gui = tk.Toplevel(main_window)
            self.gui.grab_set()
            self.gui.title("Wordle Suggestor")
            self.frame = tk.Frame(self.gui)
            self.frame.grid()

            for i in range(6):  # 6 rows in Wordle
                self.gui_add_row(i, num_letters)

            def helper() -> None:

                # if every entry has a single letter value and is not colored white (default bg color)
                if len(list(filter(lambda x: type(x) == tk.Entry and x.get().lower() in letter_list and x.cget(
                        'bg') != '#ffffff', self.frame.grid_slaves(self.counter)))) == num_letters:
                    self.error_label = None
                    self.info_label = None
                    # load input here
                    self.process(all_words, num_letters)
                    self.counter += 1
                else:  # invalid, send error message
                    self.set_error_label("Only one alphabetical\ncharacter per entry\nand choose a color.")

            button = tk.Button(self.frame, text="Submit", width=8, command=helper, background='green')
            button.grid(row=6)
            self.set_info_label(f"Your first\nsuggested word is\n{initial_suggestion}")

        def assign5():
            load(5)

        def assign6():
            load(6)

        label = tk.Label(text="Welcome to the Wordle Suggestor!\nPlease select the number of letters for the wordle!\n")
        button5 = tk.Button(self.frame, text="5 Letter Wordle", command=assign5, background='green')
        button6 = tk.Button(self.frame, text="6 Letter Wordle", command=assign6, background='green')

        label.pack()
        button5.pack()
        button6.pack()

        main_window.mainloop()
        # end gui section


if __name__ == '__main__':
    ws = Wordle_Suggestor()
    ws.main()
