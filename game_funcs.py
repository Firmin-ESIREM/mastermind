from color import Color
from random import choice
from tkinter import messagebox

possible_combinations = []


def computer_solve(palette: list[Color], combination: list[Color], combination_nb_elements: int, number_of_turns: int) -> None | int:
    possible_combinations.clear()
    combination_loop(0, combination_nb_elements, palette, [])
    previous_guesses = []
    for i in range(number_of_turns):
        guess = []
        if len(previous_guesses) == 0:
            guess = possible_combinations[0]
        else:
            for possible_combination in possible_combinations:
                valid_guess = True
                guess = possible_combination
                for previous_guess in previous_guesses:
                    correct_placements_with_previous = number_of_correct_placements(previous_guess["guess"], possible_combination)
                    correct_colors_with_previous = number_of_correct_colors(previous_guess["guess"], possible_combination)
                    if correct_placements_with_previous != previous_guess["correct_placements"] or correct_colors_with_previous != previous_guess["correct_colors"]:
                        valid_guess = False
                        break
                if valid_guess:
                    break
        correct_placements = number_of_correct_placements(combination, guess)
        if correct_placements == combination_nb_elements:
            return i + 1
        correct_colors = number_of_correct_colors(combination, guess)
        previous_guesses.append({
            "guess": guess,
            "correct_placements": correct_placements,
            "correct_colors": correct_colors
        })
    return None


def combination_loop(iteration: int, combination_nb_elements: int, palette: list[Color], colors: list[Color]):
    if iteration < combination_nb_elements:
        for color in palette:
            colors_rec = colors[:]
            colors_rec.append(color)
            combination_loop(iteration + 1, combination_nb_elements, palette, colors_rec)
    else:
        possible_combinations.append(colors)


def generate_combination(palette: list[Color], combination_nb_elements: int) -> list[Color]:
    combination = []
    for _ in range(combination_nb_elements):
        combination.append(choice(palette))
    return combination


def number_of_correct_colors(combination: list[Color], guess: list[Color]) -> int:  # White pawns
    current_combination = combination[:]
    for k, color_guess in enumerate(guess):
        if current_combination[k] == color_guess:
            current_combination[k] = ''
    number = 0
    for k, color_guess in enumerate(guess):
        if color_guess == combination[k]:
            continue
        if (color_guess in current_combination) and (current_combination[k] != color_guess):
            for i, combination_color in enumerate(current_combination):
                if combination_color == color_guess:
                    current_combination[i] = ''
                    break
            number += 1
    return number


def number_of_correct_placements(combination: list[Color], guess: list[Color]) -> int:  # Red pawns
    number = 0
    for k, element in enumerate(guess):
        if combination[k] == element:
            number += 1
    return number


def show_score(score, nb_parti):
    ratio_text = ""
    if nb_parti != 0:
        ratio = score / nb_parti
        ratio_text = f"Score moyen : {ratio}"
    messagebox.showinfo("Statistiques", f"Nombre de parties : {nb_parti}\nScore total : {score}\n{ratio_text}")
