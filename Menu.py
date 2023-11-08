import main
import matplotlib.pyplot as plt
def select_classification_scheme():
    print("Select a Classification Scheme: ")
    print(" 1. Swanson's Maintenance Tasks (SwM)")
    print(" 2. NFR Labelling")
    print(" 3. Software Evolution tasks")
    choice = int(input("Enter your choice: "))
    return choice


def select_committer(committers):
    print("Select a Committer:")
    for i, committer in enumerate(committers, start=1):
        print(f"    {i}. {committer}")

    choice = int(input(f"Enter your choice (1-{len(committers)}): "))
    if 1 <= choice <= len(committers):
        return committers[choice - 1]
    else:
        return None
def select_features(features):
    print("Select a Feature:")
    for i, feature in enumerate(features, start=1):
        print(f"    {i}. {feature}")
    choice = int(input(f"Enter your choice (1-{len(features)}): "))
    if 1 <= choice <= len(features):
        return choice-1
    else:
        return None
def scheme_feature_declaration():
    scheme_choice = select_classification_scheme()
    features = []
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
    return scheme_choice, features
def menu():
    mydict = main.data_preprocessing()
    committers = list(mydict.keys())
    while True:
        print("\nMenu:")
        print("1. Select Classification Scheme and Committer")
        print("2. Select Classification Scheme and Feature")
        print("3. Print the developer with the maximum number of commits")
        print("4. Exit")
        option = int(input("Enter your choice: "))

        if option == 1:
            scheme_choice = select_classification_scheme()
            committer = select_committer(committers)
            if committer:
                scheme = scheme_feature_declaration()[0]
                features = scheme_feature_declaration()[1]
                if committer in mydict and scheme in mydict[committer]:
                    counts = mydict[committer][scheme]
                    print(f"Commits by {scheme} for {committer}: {counts}")
                else:
                    print(f"No data found for {committer} and {scheme}.")
            else:
                print("Invalid committer selection.")

            plt.bar(features, mydict[committer][scheme])
            plt.xlabel('Features')
            plt.ylabel('Total Number of Commits')
            plt.title(f'Comparison for {committer}\'s Commits Classified by {scheme}')
            plt.show()

        elif option == 2:
            scheme_choice = select_classification_scheme()
            scheme = scheme_feature_declaration()[0]
            features = scheme_feature_declaration()[1]

            feature_choice = select_features(features)
            feature_list = []
            for name, value in mydict.items():
                feature_list.append(value[scheme][feature_choice])
            plt.figure().set_figwidth(15)
            plt.bar(committers, feature_list)
            plt.xlabel('Committers')
            plt.ylabel('Total Number of Commits')
            plt.title(f'Comparison for all developers Commits Classified by feature {feature_choice + 1}')
            plt.show()
            print()
        elif option == 3:
            scheme_choice = select_classification_scheme()
            scheme = scheme_feature_declaration()[0]
            features = scheme_feature_declaration()[1]

            feature_choice = select_features(features)
            max_names = []
            max_commit = -1
            for name, values in mydict.items():
                print(f"Committer: {name} - values: {values}")
                if values[scheme][feature_choice] > max_commit:
                    max_commit = values[scheme][feature_choice]
                    max_names = [name]
                elif values[scheme][feature_choice] == max_commit:
                    max_names.append(name)
            for name in max_names:
                print(f"\nCommitter: {name} ")
                print(f"Feature: {feature_choice + 1} - Value: {max_commit}")
        elif option == 4:
            print("Exiting the program.")
            break


if __name__ == '__main__':
    menu()