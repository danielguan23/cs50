import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    database = sys.argv[1]
    dnabase = sys.argv[2]
    strcheck = []
    profiles = []

    # TODO: Read database file into a variable
    with open(database, "r") as datafile:
        datareader = csv.DictReader(datafile)

        # possible str to check
        strcheck = datareader.fieldnames[1:]

        # load all data into an array
        datalist = list(datareader)
        # print(datalist)
        for row in datareader:
            # Add person to profiles
            profiles.append(row)

        print(profiles)


    # TODO: Read DNA sequence file into a variable
    with open(dnabase, "r") as dnafile:
        sequence = dnafile.read()
        # print(sequence)

    # TODO: Find longest match of each STR in DNA sequence
    seqcount = dict.fromkeys(strcheck, 0)

    for str in strcheck:
        seqcount[str] = longest_match(sequence, str)
    # print(seqcount)

    # TODO: Check database for matching profiles
    for person in range(len(datalist)):

        matches = 0

        for str in strcheck:
            if int(datalist[person][str]) == seqcount[str]:
                matches += 1
            else:
                continue

        # print(matches)

        if matches == len(strcheck):
            print(datalist[person]["name"])
            exit(0)

    print("No match")
    exit(2)


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
