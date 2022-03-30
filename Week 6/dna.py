import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: dna.py *.csv *.txt")
        return sys.exit(1)

    # TODO: Read database file into a variable
    csv_filename = sys.argv[1]

    subsequence = []
    with open(csv_filename) as fe:
        # Save into memory first line of .csv file.
        first_line = fe.readline().strip()
        subsequence = first_line[5:].split(",")

    dnas = []
    with open(csv_filename) as f:
        reader = csv.DictReader(f)
        for i in reader:
            dnas.append(i)

    # TODO: Read DNA sequence file into a variable
    sequence = ""
    txt_filename = sys.argv[2]

    with open(txt_filename) as fn:
        sequence = fn.readline().strip()

    # TODO: Find longest match of each STR in DNA sequence
    result = {}
    for i in subsequence:
        res = longest_match(sequence, i)
        result[i] = str(res)

    # TODO: Check database for matching profiles
    found = ""
    for i in dnas:
        test = dict(list(i.items())[1:])

        if test == result:
            found = i["name"]

    if len(found):
        print(found)
    else:
        print("No match")

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
