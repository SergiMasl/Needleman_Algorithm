#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def get_scoring_parameters():
    """
        Purpose: Gets the scoring parameters for the matrix from the user input
        Input: User input for match score, mismatch score, and gap penalty
        Output: Match score, mismatch score, and gap penalty as integers
    """
    
    print("default values for match score, mismatch score, and gap penalty are +2, -1, and -2 respectively.")
    print("You can choose to use the default values or enter your own values.")
    user_parameters = input("Do you want to use the default values? (yes/no): ")
    while user_parameters.lower() not in ["yes", "no"]:
        user_parameters = input("Invalid input. Please enter 'yes' or 'no': ")
    
    if user_parameters.lower() == "yes":
        match_score = 2
        mismatch_score = -1
        gap_penalty = -2
    else:
        try:
            match_score = int(input("Enter the match score: "))
        except ValueError:
            raise ValueError("Match score must be an integer.")

        try:
            mismatch_score = int(input("Enter the mismatch score: "))
        except ValueError:
            raise ValueError("Mismatch score must be an integer.")

        try:
            gap_penalty = int(input("Enter the gap penalty: "))
        except ValueError:
            raise ValueError("Gap penalty must be an integer.")

    return match_score, mismatch_score, gap_penalty

if __name__ == "__main__":
    tets_1 = get_scoring_parameters()
    print(tets_1)
