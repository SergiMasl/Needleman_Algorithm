def parsing(file_from_input):
    """
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
    sequences = []
    current_id = None
    current_seq = []
    
    """next step is use real fasta files to test the parsing function, and make sure it can handle multiple 
    sequences in one file, and that it can handle sequences of different lengths.
    Also need to make sure it can handle sequences with different characters (e.g. N for unknown bases)."""

    with open(file_from_input, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_id is not None:
                    sequences.append((current_id, ''.join(current_seq)))
                current_id = line[1:]
                current_seq = []
            else:
                current_seq.append(line.upper())

    if current_id is not None:
        sequences.append((current_id, ''.join(current_seq)))

    return sequences



#Sergey will be doing the parsing function(s)