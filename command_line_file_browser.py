import os
from os.path import join as pjoin

def file_browser():
    current_path = os.getcwd()
    while True:
        choice_dict = display_directory_contents(current_path)
        choice_num = None
        while True:
            choice_num = input("\nPlease select a number: ")

            # Check that the input is a number
            try:
                choice_num = int(choice_num)
            except ValueError:
                print("INVALID: Only an integer value may be input.")
                choice_num = None
                continue

            if (choice_num < 0) or (choice_num >= len(choice_dict)):
                print("INVALID: Please select a number from the above list.")
                choice_num = None
                continue

            # Number chosen must be valid, exit loop.
            break

        print("You have chosen: {}".format(choice_num))
        selected_type = choice_dict[choice_num]["type"]
        selected_item = choice_dict[choice_num]["str"]
        if selected_type == "dir":
            current_path = pjoin(current_path, selected_item)
        else:
            final_item = os.path.abspath(pjoin(current_path, selected_item))
            print("You have selected '{}'".format(final_item))
            yesno = raw_input("Is this correct? [Y/n]")
            if yesno in "yY":
                return final_item
            else:
                print("")
                continue


def display_directory_contents(dir_path):
    print("Current Directory: {}".format(os.path.abspath(dir_path)))
    dir_contents = os.listdir(dir_path)
    files = []
    directories = []
    for item in dir_contents:
        if os.path.isdir(pjoin(dir_path, item)):
            directories.append(item)
        else:
            files.append(item)
    if os.path.dirname(dir_path) != dir_path:
        directories.append("..")

    file_list = list(enumerate(sorted(files)))
    dir_list = list(enumerate(sorted(directories), len(file_list)))

    output_dir = {}
    print("Files:")
    for num, filename in file_list:
        print("{}: {}".format(num, filename))
        output_dir[num] = {"str": filename, "type": "file"}
    print("\nDirectories:")
    for num, dirname in dir_list:
        print("{}: {}".format(num, dirname))
        output_dir[num] = {"str": dirname, "type": "dir"}

    return output_dir

################################################################################
if __name__ == "__main__":
    file_browser()
