from random import randint

letter_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

color_list = ['green', 'yellow', 'blank', 'y', 'g', 'b']

init_suggestions = ["irate", "sound", "graph", "teach", "words", "sloth", "reach", "itchy", "steal", "cheat", "meats"]

print_order = {0: "first", 1: "second", 2: "third", 3: "fourth", 4: "fifth"}


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


def suggest_word(find, confirmed, remaining_dict):

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

    return remaining_dict


def check_duplicate(random_word):
    for character in random_word:
        # check whether there are duplicate characters or not
        if random_word.count(character) > 1:
            return True
    return False


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
        for i in range(0, len(output)):
            if output[i][1] == 'b' or output[i][1] == 'blank':
                for word in all_words.copy():
                    if output[i][0] in word:
                        all_words.remove(word)
            elif output[i][1] == 'y' or output[i][1] == 'yellow':
                find_positions[i] = output[i][0]
            elif output[i][1] == 'g' or output[i][1] == 'green':
                confirmed_positions[i] = output[i][0]

        all_words = suggest_word(find_positions, confirmed_positions, all_words)
        rand_option = all_words[randint(0, len(all_words) - 1)]

        if check_duplicate(rand_option):
            rand_option = all_words[randint(0, len(all_words) - 1)]

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
            print(f"Congratulations! You got the Wordle after {round + 1} tries!")
            break
        if round == 6:
            print("You did not get the Wordle :(")

        print(f'Your suggested next word is {rand_option}. ')
