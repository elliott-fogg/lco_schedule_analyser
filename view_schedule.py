import sys
import os
import argparse
from command_line_file_browser import file_browser
from format_data import obtain_dataframe

##### Deal with command line arguments, and select files #######################

file_dir = os.path.dirname(os.path.abspath(__file__))
default_path = os.path.join(file_dir, "sample_files/sample_input.json")

default_input_filepath = "data/input_request_data.json"
default_output_filepath = "data/normal_schedule_20190416024632.json"

def parse_args():
    arg_parser = argparse.ArgumentParser(
        description="Argument parser for something or other?")

    arg_parser.add_argument("-i", "--input", type=str, default=None,
        help="Provide filepath to an input file.")

    arg_parser.add_argument("-o", "--output", type=str, default=None,
        help="Provide filepath to an output file.")

    arg_parser.add_argument("-s","--select", action="store_true",
        help="Manually select a file from a TKinter screen")

    arg_parser.add_argument("-d", "--default", action="store_true",
        help="Use the default sample files.")

    args, unknown = arg_parser.parse_known_args()

    print(args)

    if len(unknown) > 0:
        print("Unknown Args: {}".format(unknown))
        print(args)

    if args.default:
        input_filepath = os.path.join(file_dir, "sample_files/sample_input.pickle")
        output_filepath = os.path.join(file_dir, "sample_files/sample_output.json")

    elif (args.input != None) and (args.output != None) and not args.select:
        input_filepath = args.input
        output_filepath = args.output

    else:
        print("Please select an input file:")
        input_filepath = file_browser()
        print("\nPlease select an output file:")
        output_filepath = file_browser()

    if not os.path.isfile(input_filepath):
        if os.path.isfile(os.path.join(file_dir, input_filepath)):
            input_filepath = os.path.join(file_dir, input_filepath)
        else:
            print("ERROR: Input file not valid - '{}'".format(input_filepath))
            return

    if not os.path.isfile(output_filepath):
        if os.path.isfile(os.path.join(file_dir, output_filepath)):
            output_filepath = os.path.join(file_dir, output_filepath)
        else:
            print("ERROR: Output file not valid - '{}'".format(output_filepath))
            return

    return (input_filepath, output_filepath)


if __name__ == '__main__':
    input, output = parse_args()
    df = obtain_dataframe(input, output)
    print("Complete")
