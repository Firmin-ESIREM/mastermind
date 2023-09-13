from json import loads
from color import Color
from game_funcs import generate_combination, number_of_correct_colors, number_of_correct_placements

with open("config.json", 'r') as f:
    config = loads(f.read())


# Init the palette from the config file
palette = []
for color in config["palette"]:
    palette.append(Color(color["name"], color["letter"], color["hex_code"]))


def find_color_by_letter(letter: str) -> Color:
    return next((x for x in palette if x.letter == letter), None)


combination = generate_combination(palette)

print(combination)

for k in range(config["number_of_turns"]):
    valid_guess = False
    guess = []
    while not valid_guess:
        guess = []
        raw_guess = input(f"Tour {k + 1} | Entrez une combinaison : ")
        if len(raw_guess) != 4:
            print("Entrée invalide, trop de caractères.")
            continue
        for character in raw_guess:
            guessed_color = find_color_by_letter(character)
            if guessed_color is not None:
                guess.append(guessed_color)
                valid_guess = True
            else:
                valid_guess = False
                print(f"Entrée invalide, couleur {character} non reconnue.")
                break
    correct_placements = number_of_correct_placements(combination, guess)
    if correct_placements == 4:
        print("C'est gagné ! Vous avez trouvé la bonne combinaison.")
        break
    correct_colors = number_of_correct_colors(combination, guess)
    print(f"Correct : {correct_placements} | Partiel : {correct_colors}")
    print("------\n")
    if k == 11:
        print("C'est perdu... Vous n'avez pas trouvé la combinaison.")
