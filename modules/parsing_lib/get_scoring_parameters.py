def get_scoring_parameters():
    """
        Purpose: Gets the scoring parameters for the matrix from the user input
        Input: User input for match score, mismatch score, and gap penalty
        Output: Match score, mismatch score, and gap penalty as integers
    """
    match_score = int(input("Enter the match score: "))
    mismatch_score = int(input("Enter the mismatch score: "))
    gap_penalty = int(input("Enter the gap penalty: "))
    
    return match_score, mismatch_score, gap_penalty

get_scoring_parameters()