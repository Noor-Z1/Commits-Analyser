# CNG445 Fall 2023
# Assignment 1: A Data Analyser for the Classification Commit Messages
# Authors: Noor Ul Zain 2528644 and Shemin Samiei 2542389
import os
import sys

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python commitsanalyser.py <file1.ext> <file2.ext>")
    sys.exit(1)

# Extract the file names from command-line arguments
commits_file = sys.argv[1]
identities_file = sys.argv[2]

# Check if the provided files exist
if not os.path.exists(commits_file) or not os.path.exists(identities_file):
    print("One or more specified files do not exist.")
    sys.exit(1)
# this function takes the arguments from the command line of the filenames
# the function then parses both the files based on the specification of the assignment
# and then creates the required dictionary hierarchy

def data_preprocessing(file1, file2):

    # this is the auxiliary dictionary where I store the unique committers (based on their names)
    # and store a list of the committer IDs they have used as the value of the key

    identities = {}
    with open(file1) as f:
        lines = f.readlines()
        for line in lines[1:]:  # skip the first line because it has the format info
            if line.split(',')[1] in identities:  # if the name is already in the dictionary
                identities[line.split(',')[1]].append(line.split(',')[0])
            else:
                identities[line.split(',')[1]] = [line.split(',')[0]]

    f.close()

    # let's create the nested dictionary with the first key being the committer name
    # and for each commiter we create a dictionary of the classified tasks

    mydict = {}

    for name in identities:
        mydict[name] = {"SwM tasks": [0, 0, 0], "NFR Labelling": [0, 0, 0, 0, 0, 0], "SoftEvol tasks": [0, 0, 0, 0]}

    # Now we pre-process the commits file and fill the nested dictionary

    with open(file2) as f:
        lines = f.readlines()

        for line in lines[1:]:
            l = line.split(',')

            # first we find based on the committer ID, the committer name using the aux dictionary we created before
            for name, values in identities.items():
                if l[14] in values:
                    found_name = name
                    break  # we found the committer name

            # now we fill the nested dictionary, updating the counters for the specified
            # classification schemes based on the found committer
            for name, values in mydict[found_name].items():
                if name == "SwM tasks":
                    mydict[found_name][name][0] += int(l[1])
                    mydict[found_name][name][1] += int(l[2])
                    mydict[found_name][name][2] += int(l[3])
                elif name == "NFR Labelling":
                    mydict[found_name][name][0] += int(l[4])
                    mydict[found_name][name][1] += int(l[5])
                    mydict[found_name][name][2] += int(l[6])
                    mydict[found_name][name][3] += int(l[7])
                    mydict[found_name][name][4] += int(l[8])
                    mydict[found_name][name][5] += int(l[9])
                elif name == "SoftEvol tasks":
                    mydict[found_name][name][0] += int(l[10])
                    mydict[found_name][name][1] += int(l[11])
                    mydict[found_name][name][2] += int(l[12])
                    mydict[found_name][name][3] += int(l[13])

    f.close()

    return mydict


def main():
    mydict = data_preprocessing(identities_file ,commits_file)
    print(mydict)


if __name__ == '__main__':
    main()