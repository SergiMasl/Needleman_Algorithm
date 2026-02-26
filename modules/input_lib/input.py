
import argparse 
import sys 

def read_two_fastas(file1: str, file2: str) -> tuple[str,str]:
    """ Parses through sequences input for CLI tool. 
    Opening files and parsing headers and spaces.
    If no files found, returning Error. """
    sequences = []
    try: 
        for filepath in (file1, file2):              #reading two fasta files 
            with open(filepath, "r") as f:
                lines = f.readlines()

            if lines[0].startswith(">"):       #removing fasta headers
                lines = lines[1:]

            sequence = "".join(line.strip() for line in lines)   # removing newline char and whitespace
            sequences.append(sequence)                            

    except FileNotFoundError as error:                               # Checking if file is found; if not gives an error message 
        sys.exit(f"Error: File not found: {error.filename}")
    return tuple(sequences) 

if __name__ == "__main__":
    file1 = "ex_seq.fasta"
    file2 = "ex_seq2.fasta"
    seq1, seq2 = read_two_fastas(file1, file2)
    sys.stdout.write(f"Sequences successfully read:\n")
    sys.stdout.write(f"Sequence 1: {seq1}\n")
    sys.stdout.write(f"Sequence 2: {seq2}\n")

# Function called twice for two separate fasta files or pasted sequences (for further parsing)
# Function for pasting two sequences will be created after 

    #Alyssa will be doing the input function(s)    