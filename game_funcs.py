from color import Color
from random import choice


def generate_combination(palette: list[Color]) -> list[Color]:
    combination = []
    for _ in range(4):
        combination.append(choice(palette))
    return combination


def number_of_correct_colors(combination: list[Color], guess: list[Color]) -> int:  # White pawns
    current_combination = combination[:]
    for k, color_guess in enumerate(guess):
        if current_combination[k] == color_guess:
            current_combination[k] = ''
    number = 0
    for k, color_guess in enumerate(guess):
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

