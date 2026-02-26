def parsing(file_from_input):
    """
     -this function will take one array which contain 2 seqs arrays

        Purpose: Puts the two DNA sequences in a table-like array
        Input: Taking the two DNA sequences from the User Input File output
        Output: Scoring values for the matrix and rank top three choices 
       
        High-level steps: 
        -    Calculate the scoring values for the matrix
        -    Score the values properly and be able to tabulate properly
        -    No data table mismatch or shifts
        -    Be able to compensate if the sequence lengths are not the same 
        -    Be capable of performing a traceback (multiple tracebacks if required) to find the most aligned sequences
        -    Be able to rank the top three choices(?), and have tie-rank capabilities 

    """
    
    """next step is use real fasta files to test the parsing function, and make sure it can handle multiple 
    sequences in one file, and that it can handle sequences of different lengths.
    Also need to make sure it can handle sequences with different characters (e.g. N for unknown bases)."""

    ###change to match and mismatch scoring values, and gap penalties, and make sure it can handle those properly in the scoring matrix and traceback functions.

    
    pass


#step 1: ask user asking user for match score, mismatch score, and gap penalty  
#match_score, mismatch_score, gap_penalty = get_scoring_parameters()



#Sergey will be doing the parsing function(s)