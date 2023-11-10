from dictionaries import *
import os
import sys
import matplotlib.pyplot as plt

# Check if the correct number of command-line arguments is provided
if len(sys.argv) != 3:
    print("Usage: python dictionaries.py <file1.ext> <file2.ext>")
    sys.exit(1)

# Extract the file names from command-line arguments
commits_file = sys.argv[1]
identities_file = sys.argv[2]

# Check if the provided files exist
if not os.path.exists(commits_file) or not os.path.exists(identities_file):
    print("One or more specified files do not exist.")
    sys.exit(1)
'''
Since the menu asks for selecting the scheme 
few times I created a separate function for that
'''
def select_classification_scheme():
    print("\nSelect a Classification Scheme: ")
    print(" 1. Swanson's Maintenance Tasks (SwM)")
    print(" 2. NFR Labelling")
    print(" 3. Software Evolution tasks")
    choice = int(input("Enter your choice:\n"))
    return choice
'''
This function takes the committers list from the dictionary 
and displays them on the screen in order for the user to choose
one and returns user's choice
'''
def select_committer(committers):
    print("Select a Committer:")
    for i, committer in enumerate(committers, start=1):
        print(f"    {i}. {committer}")

    choice = int(input(f"\nEnter your choice (1-{len(committers)}): "))
    if 1 <= choice <= len(committers):
        return committers[choice - 1]
    else:
        return None
#Same approach as (committer) goes for this function
def select_features(features):
    print("Select a Feature:")
    for i, feature in enumerate(features, start=1):
        print(f"    {i}. {feature}")
    choice = int(input(f"Enter your choice (1-{len(features)}):\n "))
    if 1 <= choice <= len(features):
        return choice-1
    else:
        return None

'''
this function returns the name of the feature that user already selected
(since it is not available in the dictionary)
it will be used to be displayed on the bar chart/screen
'''
def get_feature_name(features,choice):
    name = ''
    for i, feature in enumerate(features, start=1):
        if choice+1 == i:
            name = feature
            break
    return name
'''
since the user needs to see and select 
the scheme with its related features
a tuple will be returned and used for
both of them using this function
'''
def scheme_feature_declaration():
    scheme_choice = select_classification_scheme()
    features = []
    scheme = ''
    if scheme_choice == 1:
        scheme = "SwM tasks"
        features = ["Corrective Tasks", "Adaptive Tasks", "Perfective Tasks"]
    elif scheme_choice == 2:
        scheme = "NFR Labelling"
        features = ["Maintainability", "Usability", "Functionality", "Reliability", "Efficiency",
                    "Portability"]
    elif scheme_choice == 3:
        scheme = "SoftEvol tasks"
        features = ["Forward Engineering", "Re-Engineering", "Corrective Engineering", "Management"]
    return scheme, features
def menu():
    #getting the dictionary(using the files declared from cmd line)
    #and retrieving the committers' names as a list from the dictionary
    mydict = data_preprocessing(identities_file, commits_file)
    committers = list(mydict.keys())
    while True:
        print("\nMenu:")
        print("1. Select Classification Scheme and Committer")
        print("2. Select Classification Scheme and Feature")
        print("3. Print the developer with the maximum number of commits")
        print("4. Exit")
        option = int(input("Enter your choice: \n"))

        if option == 1:
            committer = select_committer(committers)
            #scheme and features are needed for the bar chart
            scheme = ''
            features = []
            if committer:
                '''since the select_scheme function
                (which has print() function in it) 
                is used inside scheme_feature_declaration
                I used a temp value to get the tuple 
                (not to have repetition) and 
                use it relatively for scheme and features'''
                temp = scheme_feature_declaration()
                scheme = temp[0] #selected scheme by the user
                features = temp[1] #features names list related to scheme
                if committer in mydict and scheme in mydict[committer]:
                    counts = mydict[committer][scheme]
                    print(f"Commits by {scheme} for {committer}: {counts}")
                else:
                    print(f"No data found for {committer} and {scheme}.")
            else:
                print("Invalid committer selection.")
            plt.figure().set_figwidth(10)
            plt.bar(features, mydict[committer][scheme])
            plt.xlabel('Features')
            plt.ylabel('Total Number of Commits')
            plt.title(f'Comparison for {committer}\'s Commits Classified by {scheme}')
            plt.show()
        elif option == 2:
            temp = scheme_feature_declaration()
            scheme = temp[0] #selected scheme by the user
            features = temp[1] #features names list related to scheme
            feature_choice = select_features(features) #selected feature by the user (a number)
            feature_name = get_feature_name(features,feature_choice) #selected feature by the user (Name)
            feature_list = [] #needed for bar chart
            '''Retrieved the values of the feature that 
            user selected from the dictionary with a loop.
            This list will be used for creating the numbers
            on the bar chart'''
            for name, value in mydict.items():
                feature_list.append(value[scheme][feature_choice])
            plt.figure().set_figwidth(15)
            plt.bar(committers, feature_list)
            plt.xlabel('Committers')
            plt.ylabel('Total Number of Commits')
            plt.title(f'Comparison for all developers Commits Classified by {feature_name} feature ')
            plt.show()
            print()
        elif option == 3:
            temp = scheme_feature_declaration()
            scheme = temp[0] #selected scheme by the user
            features = temp[1] #features names list related to scheme
            feature_choice = select_features(features) #selected feature by the user (a number)
            feature_name = get_feature_name(features, feature_choice) #selected feature by the user (Name)
            '''these two variables are needed to keep track of the 
            committer's name and his/her commits'''
            max_names = [] #It is a list because two/more committers can have the same #of commits
            max_commit = -1 #initial value to compare should be a negative number
            for name, values in mydict.items():
                if values[scheme][feature_choice] > max_commit:
                    max_commit = values[scheme][feature_choice]
                    max_names = [name]
                elif values[scheme][feature_choice] == max_commit:
                    max_names.append(name)
            for name in max_names:
                print(f"\nCommitter: {name} ")
                print(f"Feature: {feature_name} - Value: {max_commit}")
        elif option == 4:
            print("Exiting the program.")
            break

if __name__ == '__main__':
    menu()
