from random import randint

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

color_list = ['green', 'yellow', 'blank', 'y', 'g', 'b']

init_suggestions = ["irate", "sound", "graph", "teach", "words", "sloth", "reach", "itchy", "steal", "cheat", "meats"]

print_order = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth"}


letter_values = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3,
                 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4,
                 'z': 10}


def load_dictionary():
    init_dict = []
    with open("dictionary.txt", "r") as file:
        line = "line"
        while line != '':  # EOF
            line = file.readline().rstrip()
            init_dict.append(line)
    return init_dict


def load_input(all):
    output = {}
    word_guess = ""
    while True:
        for i in range(0, 5):
            print(f'Input the {print_order[i]} letter of your guess: ')
            letter = input().lower()
            while letter not in letter_list:
                print("Please type a single letter followed by 'enter': ")
                letter = input().lower()

            word_guess += letter
            print("Input the color (Yellow, Green, Blank)")
            color = input().lower()
            while color not in color_list:
                print("Please type either Yellow (y), Green (g), or Blank (b): ")
                color = input().lower()

            output[i] = [letter, color]
        if word_guess not in all:
            print(f"{word_guess} is not a valid guess. Please double check your input for correctness.\n\n")
            word_guess = ""
        else:
            break
    return output


def suggest_word(find, confirmed, remove, remaining_dict):

    # try:
    #     del remaining_dict['']
    # except KeyError:
    #     print("")

    for position, letter in confirmed.items():
        for guess in remaining_dict.copy():
            if guess.find(letter, position) != position:
                remaining_dict.remove(guess)

    for position, letter in find.items():
        for guess in remaining_dict.copy():
            if guess.find(letter, position) == position:
                remaining_dict.remove(guess)
            elif letter not in guess:
                remaining_dict.remove(guess)

    for position, letter in remove.items():
        for guess in remaining_dict.copy():
            if letter in guess and letter not in confirmed.values() and letter not in find.values():
                remaining_dict.remove(guess)

    return remaining_dict


def check_duplicate(random_word):
    for character in random_word:
        # check whether there are duplicate characters or not
        if random_word.count(character) > 1:
            return True
    return False


def calculate_values(remaining_words, positions, find_pos, confirmed_pos):
    value_dictionary = {}
    for word in remaining_words:
        word_value = 0
        for letter in word:
            word_value += letter_values[letter]
        value_dictionary[word] = word_value

    # make value zero (first priority) if there is a yellow highlighted letter in a non-confirmed space
    for word in remaining_words:
        for pos in positions:
            for letter in find_pos.values():
                if word.find(letter, pos) not in list(confirmed_pos.keys()):
                    value_dictionary[word] = 0

    v_dict = {}
    for k, v in value_dictionary.items():
        v_dict[v] = [key for key, value in value_dictionary.items() if value == v]

    return dict(sorted(v_dict.items(), key=lambda item: item[0]))


def find_rand_suggestion(suggestions):
    return suggestions[list(suggestions.keys())[0]][randint(0, len(suggestions[list(suggestions.keys())[0]]) - 1)]


def print_welcome():
    print("Welcome to the Wordle Suggestor!\nFollow the prompts for your word suggestion!")


if __name__ == '__main__':

    print_welcome()
    all_words = load_dictionary()
    suggestion = init_suggestions[randint(0, len(init_suggestions) - 1)]

    print(f'Try this word for your initial guess: {suggestion}')
    print("Type '1' to continue. Or, for a different initial suggestion, type '2'.")

    option = input()
    while option != '1':
        while option != '1' and option != '2':
            print("Please type '1' or '2': ")
            option = input()

        if option == '2':
            suggestion = init_suggestions[randint(0, len(init_suggestions) - 1)]

        print(f'Try this word for your initial guess: {suggestion}')
        print("Type '1' to continue. Or, for a different initial suggestion, type '2'.")
        option = input()

    round = 0
    while round < 6:

        output = load_input(all_words)
        find_positions = {}
        confirmed_positions = {}
        remove_positions = {}
        for i in range(0, len(output)):
            if output[i][1] == 'y' or output[i][1] == 'yellow':
                find_positions[i] = output[i][0]
            elif output[i][1] == 'g' or output[i][1] == 'green':
                confirmed_positions[i] = output[i][0]
            elif output[i][1] == 'b' or output[i][1] == 'blank':
                remove_positions[i] = output[i][0]

        to_remove = list(confirmed_positions.keys())
        positions_to_check = [x for x in [0, 1, 2, 3, 4] if x not in to_remove]

        all_words = suggest_word(find_positions, confirmed_positions, remove_positions, all_words)
        new_suggestion = calculate_values(all_words, positions_to_check, find_positions, confirmed_positions)

        rand_option = find_rand_suggestion(new_suggestion)

        if round < 4 and check_duplicate(rand_option):
            rand_option = find_rand_suggestion(new_suggestion)

        if rand_option == "":
            print("There are no suggested words available. Please double check that you input your information "
                  "correctly.")
            exit(0)

        print("Type '1' to continue to the next round or type '2' if you got the wordle!")

        round += 1
        a = input()
        while a != '1' and a != '2':
            print("Please type '1' or '2': ")
            a = input()
        if a == '2':
            print(f"Congratulations! You got the Wordle after {round} tries!")
            break
        if round == 6:
            print("You did not get the Wordle :(")

        print(f'Your suggested next word is {rand_option}. ')
