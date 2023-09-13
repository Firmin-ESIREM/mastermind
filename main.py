from json import loads
from color import Color
from game_funcs import generate_combination, number_of_correct_colors, number_of_correct_placements, show_score
from sys import exit as sys_exit
from os.path import isfile

with open("config.json", 'r') as f:
    config = loads(f.read())

# Init the palette from the config file
palette = []
for color in config["palette"]:
    palette.append(Color(color["name"], color["letter"], color["hex_code"]))

combination_nb_elements = config["number_of_elements_in_the_combination"]
number_of_turns = config["number_of_turns"]


def init():
    for file_name in [".nb_parti", ".score"]:
        with open(file_name, 'w') as f:
            f.write("0")
    print("Fichiers de statistique (ré)initialisés.")


def find_color_by_letter(letter: str) -> Color:
    return next((x for x in palette if x.letter == letter), None)


if not (isfile("nb_parti.txt")) or not (isfile("score.txt")):
    init()

print(f"""
    ###################
    #                 #
    #   MASTERMIND    #
    #                 #
    ###################

Nombre d'essais : {number_of_turns}.
Nombre de couleurs dans la combinaison : {combination_nb_elements}.
""")

stat = {}
for file in ["nb_parti", "score"]:
    with open('.' + file, 'r') as f:
        stat[file] = int(f.read())
show_score(stat["score"], stat["nb_parti"])


def game():
    combination = generate_combination(palette, combination_nb_elements)
    i = 0
    while i < number_of_turns:
        i += 1
        valid_guess = False
        guess = []
        while not valid_guess:
            guess = []
            raw_guess = input(f"Tour {i} | Entrez une combinaison : ")
            if len(raw_guess) != combination_nb_elements:
                print("Entrée invalide, mauvais nombre de caractères.")
                continue
            for character in raw_guess:
                guessed_color = find_color_by_letter(character.upper())
                if guessed_color is not None:
                    guess.append(guessed_color)
                    valid_guess = True
                else:
                    valid_guess = False
                    print(f"Entrée invalide, couleur {character} non reconnue.")
                    break
        correct_placements = number_of_correct_placements(combination, guess)
        if correct_placements == combination_nb_elements:
            print("\nC'est gagné ! Vous avez trouvé la bonne combinaison.\n")
            break
        correct_colors = number_of_correct_colors(combination, guess)
        print(f"Correct : {correct_placements} | Partiel : {correct_colors}")
        print("------\n")
        if i == 12:
            print("\nC'est perdu... Vous n'avez pas trouvé la combinaison.\n")

    for file_name in ["nb_parti", "score"]:
        with open('.' + file_name, 'r') as f:
            stat[file_name] = int(f.read())

    stat["score"] += i
    stat["nb_parti"] += 1
    for file_name in ["nb_parti", "score"]:
        with open('.' + file_name, 'w') as f:
            f.write(str(stat[file_name]))

    show_score(stat["score"], stat["nb_parti"])
    input_valid = False
    while not input_valid:
        menu = input("\nVoulez-vous reJouer (J), Remettre les stats à zéro (R) ou Quitter (Q) : ")
        menu = menu.upper()
        if menu == 'J':
            input_valid = True
            game()
        elif menu == 'R':
            input_valid = True
            init()
            game()
        elif menu == 'Q':
            input_valid = True
        else:
            print("Veuillez entrer une réponse valide.")


main_menu = input("Voulez-vous jouer (J), Remettre les stats à zéro (R) ou Quitter (Q) : ")
main_menu = main_menu.upper()
if main_menu == 'J':
    game()
elif main_menu == 'R':
    init()
    game()
else:
    sys_exit(0)
