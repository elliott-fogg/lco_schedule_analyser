import sys
import os
import argparse

file_dir = os.path.dirname(os.path.abspath(__file__))
default_path = os.path.join(file_dir, "sample_files/sample_input.json")

default_input_filepath = "data/input_request_data.json"
default_output_filepath = "data/normal_schedule_20190416024632.json"

def parse_args():
    arg_parser = argparse.ArgumentParser(
        description="Argument parser for something or other?"
    )

    arg_parser.add_argument("file_location", nargs="*",
        help="provide a filepath for an input file")

    arg_parser.add_argument("-s","--select", action="store_true",
        help="manually select a file from a TKinter screen")

    args, unknown = arg_parser.parse_known_args()

    print(args)

    if len(unknown) > 0:
        print("Unknown Args: {}".format(unknown))
        print(args)

    if args.select:
        # print("Open Tkinter dialog box")
        print("The --select option has not yet been implemented.")

        # This is proving a little harder than anticipated.
        # Possible options:
            # Manage to incorporate the system-installed tkinter into the
            #   virtualenv, by using --include-site-packages. Unknown if this
            #   will unintentionally taint the virtualenv.
            # Create a command-line based file explorer tool. Not the most
            #   desirable. Potentially pointless, but allows for not typing
            #   everything out.
            # Give up, just manually type the relative path to the file as a
            #   command line argument. We'll leave it with this for now.

    # else:
    if len(args.file_location) == 1:
        filepath = os.path.join(file_dir, args.file_location[0])
        if os.path.isfile(filepath) and filepath.endswith(".json"):
            print("Using file '{}'".format(filepath))
            return filepath

        else:
            print("Provided file is invalid: '{}'".format(filepath))
            return None

    else:
        filepath = default_path
        if os.path.isfile(filepath) and filepath.endswith(".json"):
            print("Using default file '{}'".format(filepath))
            return filepath

        else:
            print("Default filepath is invalid: '{}'".format(filepath))
            return None

if __name__ == '__main__':
    filepath = parse_args()
    print("Complete")
