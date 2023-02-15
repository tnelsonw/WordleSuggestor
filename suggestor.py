
from random import randint
from typing import List
from collections import Counter
from enum import Enum

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

init_suggestions5 = ["irate", "sound", "graph", "teach", "words", "sloth", "reach", "itchy", "steal", "cheat", "meats",
                     "arise", "raise"]

init_suggestions6 = ["satire", "aspire", "mouthy", "plough", "amends", "tricky", "wavier"]

print_order = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth", 5: "sixth"}

# based on commonality of each letter
letter_values = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3,
                 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4,
                 'z': 10}


class Color(Enum):
    YELLOW = ("yellow", "y")
    GREEN = ("green", "g")
    BLANK = ("blank", "b")


color_list = Color.YELLOW.value + Color.GREEN.value + Color.BLANK.value


def load_dictionary(number: int) -> List[str]:
    """Takes a number and loads the corresponding word dictionary, returning it as a list of strings."""
    file_name = "dictionary" + str(number) + ".txt"
    with open(file_name) as file:
        return [line.rstrip() for line in file.readlines()]


def get_init_suggestion(number: int) -> str:
    """Must input integer of 5 or 6. Outputs a randomly suggested string with length of the input number"""
    if number == 5:
        return init_suggestions5[randint(0, len(init_suggestions5) - 1)]
    elif number == 6:
        return init_suggestions6[randint(0, len(init_suggestions6) - 1)]


def check_duplicate(word: str) -> bool:
    """Returns true if there are duplicate letters in a word, otherwise returns false."""
    return max(Counter(word).values()) > 1


def load_input(all_words: List[str], num: int) -> dict:
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


def suggest_word(find: dict, confirmed: dict, remove: dict, remaining_words: List[str]) -> List[str]:
    """Reduces the amount of remaining words by eliminating words that are impossible based on the input."""
    if "" in remaining_words:
        remaining_words.remove("")

    # remove words that don't have a matching letter to the confirmed (green) positions
    for position, letter in confirmed.items():
        for word in remaining_words.copy():
            if word.find(letter, position) != position:
                remaining_words.remove(word)

    # remove the word if the letter found (yellow) is at that same position (it should be elsewhere in the word
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
            p = word.find(letter, position)
            if p == position:
                remaining_words.remove(word)
                # for the rest of the word, requires more checks (could be yellow or green in other positions)
                # match the position to confirmed positions here
            elif p in remove.keys():
                remaining_words.remove(word)
            elif letter in word and letter not in confirmed.values() and letter not in find.values():
                remaining_words.remove(word)
    return remaining_words


def find_rand_suggestion(suggestions: List[str]) -> str:
    return suggestions[randint(0, len(suggestions)-1)]


def calculate_values(remaining_words: List[str], positions_to_check: List[int] = [], find_pos: dict = {},
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
    # {5: ['raise', 'arise', 'irate'], 7: ['meats', 'beats']...etc}
    v_dict = {}
    for k, v in value_dictionary.items():
        v_dict[v] = [key for key, value in value_dictionary.items() if value == v]

    # return the list with the lowest key as these are the most likely candidates
    return v_dict[min(v_dict.keys())]


def print_init_guess(init_suggestion: str) -> None:
    print(f'Try this word for your initial guess: {init_suggestion}')
    print("Type '1' to continue. Or, for a different initial suggestion, type '2'.")


def print_welcome():
    print("Welcome to the Wordle Suggestor!\n"
          "Please enter the number of letters you would like for your wordle!\n"
          "Valid number of letters are 5 and 6.\n"
          "Afterwards, please follow the prompts for your word suggestion!")


def main():
    print_welcome()

    num_letters = int(input())
    while num_letters != 5 and num_letters != 6:
        print("Please input a valid number of letters. Either 5 or 6.\n")
        num_letters = int(input())

    all_words = load_dictionary(num_letters)
    initial_suggestion = get_init_suggestion(num_letters)

    print_init_guess(initial_suggestion)

    option = input()
    while option != '1':
        while option != '1' and option != '2':
            print("Please type '1' or '2': ")
            option = input()

        if option == '2':
            initial_suggestion = get_init_suggestion(num_letters)
            print_init_guess(initial_suggestion)
            option = input()

    round = 0
    while round < num_letters + 1:

        guess_output = load_input(all_words, num_letters)
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
        all_words = suggest_word(find_positions, confirmed_positions, remove_positions, all_words)
        new_suggestions = calculate_values(all_words, positions_to_check, find_positions, confirmed_positions)
        rand_option = find_rand_suggestion(new_suggestions)

        if round < 4 and check_duplicate(rand_option):
            rand_option = find_rand_suggestion(new_suggestions)

        if rand_option == "":
            print("There are no suggested words available. Please double check that you input your information "
                  "correctly.")
            exit(0)

        print(f"There are {len(all_words)} possible words remaining.")
        print("Type '1' to continue to the next round or type '2' if you got the wordle! Type 3 to get a new "
              "suggested word.")
        print(f'Your suggested next word is {rand_option}. ')

        round += 1
        a = input()
        while a != '1' and a != '2' and a != '3':
            print("Please type '1' or '2' or '3': ")
            a = input()
        if a == '2':
            if round == 1:
                print("Congratulations! You got the Wordle after 1 try!")
            else:
                print(f"Congratulations! You got the Wordle after {round} tries!")
            break
        while a == '3':
            rand_option = find_rand_suggestion(new_suggestions)
            print("Type '1' to continue to the next round or type '2' if you got the wordle! Type 3 to get a new "
                  "suggested word.")
            print(f'Your suggested next word is {rand_option}. ')
            a = input()
            while a != '1' and a != '2' and a != '3':
                print("Please type '1' or '2' or '3': ")
                a = input()
        if round == num_letters:
            print("You did not get the Wordle :(")


if __name__ == '__main__':
    main()
