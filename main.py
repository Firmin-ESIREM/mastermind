from json import loads
from color import Color
from game_funcs import generate_combination, number_of_correct_colors, number_of_correct_placements, show_score, \
    computer_solve
from os.path import isfile
from tkinter import messagebox, Tk, Button, Label, simpledialog, Canvas, W, E
from tkinter.font import Font

main_window = Tk(className="mastermind-main")
main_window.eval('tk::PlaceWindow . center')
main_window.title("MASTERMIND")

with open("config.json", 'r') as f:
    config = loads(f.read())

# Initialize the palette from the config file
palette = []
for color in config["palette"]:
    palette.append(Color(color["name"], color["letter"], color["hex_code"]))

combination_nb_elements = config["number_of_elements_in_the_combination"]
number_of_turns = config["number_of_turns"]

stat = {}


def init():
    """
    This function initializes the score files to zero.
    :return:
    """
    for file_name in ["nb_parties", "score"]:
        with open('.' + file_name, 'w') as f:
            f.write('0')
            stat[file_name] = 0
    messagebox.showinfo("Statistiques", "Fichiers de statistiques (ré)initialisés.")


def find_color_by_letter(letter: str) -> Color:
    """
    This function allows to find a color by its abbreviation letter among the configured colors.
    :param letter:
    :return:
    """
    return next((x for x in palette if x.letter == letter), None)


if not (isfile(".nb_parties")) or not (isfile(".score")):
    init()

for file in ["nb_parties", "score"]:
    with open('.' + file, 'r') as f:
        stat[file] = int(f.read())

window_elements = []


def game():
    """
    This function defines the course of the game.
    :return:
    """
    for window_element in window_elements:
        window_element.destroy()
    window_elements.clear()
    combination = generate_combination(palette, combination_nb_elements)
    # print(combination)
    computer_number_of_turns = computer_solve(palette, combination, combination_nb_elements, number_of_turns)
    if computer_number_of_turns is None:
        found_string = "L'ordinateur n'a pas trouvé."
    else:
        found_string = f"L'ordinateur a trouvé en {computer_number_of_turns} coup{'s' if computer_number_of_turns > 1 else ''}."
    messagebox.showinfo("Résolution automatique", found_string)
    i = 0
    while i < number_of_turns:
        i += 1
        valid_guess = False
        guess = []
        while not valid_guess:
            guess = []
            raw_guess = simpledialog.askstring(f"Tour {i}", f"Entrez une combinaison.")
            if len(raw_guess) != combination_nb_elements:
                messagebox.showerror("Entrée invalide", "Mauvais nombre de caractères.")
                continue
            for character in raw_guess:
                guessed_color = find_color_by_letter(character.upper())
                if guessed_color is not None:
                    guess.append(guessed_color)
                    valid_guess = True
                else:
                    valid_guess = False
                    messagebox.showerror("Entrée invalide", f"Couleur {character} non reconnue.")
                    break
        correct_placements = number_of_correct_placements(combination, guess)
        correct_colors = number_of_correct_colors(combination, guess)
        drawing_canvas = Canvas(main_window, width=210, height=30)
        drawing_canvas.pack()
        window_elements.append(drawing_canvas)
        drawing_canvas.create_text(20, 15, font=Font(size=10), fill="#c0392b", text=str(correct_placements), anchor=W)
        drawing_canvas.create_text(200, 15, font=Font(size=10), fill="#000000", text=str(correct_colors), anchor=E)
        for k, guessed_color in enumerate(guess):
            drawing_canvas.create_oval(51 + 30 * k, 6, 69 + 30 * k, 24, fill='#' + guessed_color.hex_code, outline="")
        if correct_placements == combination_nb_elements:
            messagebox.showinfo("C'est gagné !",
                                f"Vous avez trouvé la bonne combinaison en {i} coup{'s' if i > 1 else ''}.")
            break
        if i == 12:
            combination_string = ''
            for combination_color in combination:
                combination_string += str(combination_color)
            messagebox.showinfo("C'est perdu...",
                                f"Vous n'avez pas trouvé la combinaison.\nIl s'agissait de {combination_string}.")

    if computer_number_of_turns is None:
        stat["score"] += (i - number_of_turns)
    else:
        stat["score"] += (i - computer_number_of_turns)
    stat["nb_parties"] += 1
    for file_name in ["nb_parties", "score"]:
        with open('.' + file_name, 'w') as f:
            f.write(str(stat[file_name]))

    for window_element in window_elements:
        window_element.destroy()
    window_elements.clear()
    window_elements.append(Button(main_window, text="Rejouer", command=game))
    window_elements.append(Button(main_window, text="Réinitialiser les statistiques", command=init))
    window_elements.append(Button(main_window, text="Voir les statistiques",
                                  command=lambda: show_score(stat["score"], stat["nb_parties"])))
    window_elements.append(Button(main_window, text="Quitter", command=main_window.destroy))
    for window_element in window_elements:
        window_element.pack()

available_colors = "Couleurs disponibles :"
window_elements.append(Label(main_window, text=f"Nombre d'essais : {number_of_turns}"))
window_elements.append(Label(main_window, text=f"Nombre de couleurs dans la combinaison : {combination_nb_elements}"))
for color in palette:
    available_colors += f" {color.name} ({color.letter}),"
available_colors = available_colors[:-1]
window_elements.append(Label(main_window, text=available_colors))
window_elements.append(Button(main_window, text="Jouer", command=game))
window_elements.append(Button(main_window, text="Réinitialiser les statistiques", command=init))
window_elements.append(
    Button(main_window, text="Voir les statistiques", command=lambda: show_score(stat["score"], stat["nb_parties"])))
window_elements.append(Button(main_window, text="Quitter", command=main_window.destroy))

for element in window_elements:
    element.pack()

main_window.mainloop()
