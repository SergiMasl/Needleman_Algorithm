#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from typing import Tuple

def get_scoring_parameters() -> Tuple[int, int, int]:
    """
        Purpose: Gets the scoring parameters for the matrix from the user input
        Input: User input for match score, mismatch score, and gap penalty
        Output: Match score, mismatch score, and gap penalty as integers
    """
    
    sys.stdout.write("default values for match score, mismatch score, and gap penalty are +2, -1, and -2 respectively.\n")
    sys.stdout.write("You can choose to use the default values or enter your own values.\n")
    user_parameters = input("Do you want to use the default values? (yes/no): ")
    while user_parameters.lower() not in ["yes", "no"]:
        user_parameters = input("Invalid input. Please enter 'yes' or 'no': ")
    
    if user_parameters.lower() == "yes":
        match_score = 2
        mismatch_score = -1
        gap_penalty = -2
    else:
        def prompt_int(prompt: str) -> int:
            while True:
                raw = input(prompt).strip()
                try:
                    return int(raw)
                except ValueError:
                    sys.stdout.write("Invalid input. Please enter a whole number (e.g. 2, -1, +3).\n")

        match_score    = prompt_int("Enter the match score: ")
        mismatch_score = prompt_int("Enter the mismatch score: ")
        gap_penalty    = prompt_int("Enter the gap penalty: ")

    return match_score, mismatch_score, gap_penalty

if __name__ == "__main__":
    tets_1 = get_scoring_parameters()
    sys.stdout.write(str(tets_1) + "\n")
