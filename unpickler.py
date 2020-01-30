import pickle, sys, io, contextlib, json, os
from os.path import join as pjoin

_dir = os.path.dirname(os.path.abspath(__file__))
default_scheduler_directory = pjoin(_dir, "../scheduler")

def get_scheduler_directory():
    global default_scheduler_directory
    return default_scheduler_directory
    # TODO: Add option to select directory using TKinter if not found.

def load_scheduler_directory(scheduler_directory):
    sys.path.insert(0, scheduler_directory)
    import adaptive_scheduler

### Load and Save files ########################################################

def load_pickled_file(filepath, adaptive_scheduler=False):
    if adaptive_scheduler:
        scheduler_directory = get_scheduler_directory()
        load_scheduler_directory(scheduler_directory)

    with open(filepath, "rb") as f:
        data = pickle.load(f)
    return data

def save_pickled_file(data, filepath):
    with open(filename, "wb") as f:
        pickle.dump(data, f)
    print("Pickled data to '{}'".format(filepath))

def load_json_file(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def save_json_file(data, filepath):
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print("Saved data as JSON at '{}'".format(filepath))

### Converting Pickled files to JSON-serializable objects ######################

def convert_to_json(input_value):
    if isinstance(input_value, dict):
        output_value = {}
        for key in input_value:
            output_value[str(key)] = convert_to_json(input_value[key])

    elif isinstance(input_value, list):
        output_value = []
        for item in input_value:
            output_value.append(convert_to_json(item))

    else:
        try:
            attributes = vars(input_value)
            output_value = {attr:convert_to_json(val) for
                attr, val in attributes.items()}
            output_value["__TYPE__"] = str(type(input_value))
            output_value["__AS_STRING__"] = "{}".format(input_value)

        except AttributeError:
            output_value = make_string(input_value)

    return output_value


def make_string(input_value):
    try:
        output_value = "{}".format(input_value)

    except ValueError:
        output_value = "FAILED_CONVERSION"

    return output_value


def filename_pickle_to_json(filepath):
    return filepath.replace(".pickle", ".json")


def convert_pickle_to_json(filepath):
    data = load_pickled_file(filepath, True)
    json_data = convert_to_json(data)
    output_filepath = filename_pickle_to_json(filepath)
    save_json_file(json_data, output_filepath)


################################################################################

if __name__ == "__main__":

    try:
        shell = get_ipython()
        ipython = True
    except NameError:
        ipython = False

    if len(sys.argv) == 1 and ipython:
        print("Loaded Unpickler functions into memory.")
        # TODO: Add option to select file using TkInter

    elif len(sys.argv) == 2:
        filepath = sys.argv[1]
        print('working...')

        if ipython:
            data = load_pickled_file(filepath, True)
            print("file '{}' unpickled to var 'data'".format(filepath))

        else:
            convert_pickle_to_json(filepath)

    else:
        print("Incorrect number of command line arguments: {}".format(sys.argv))
        print("Please specify one file to unpickle, or load the module in IPython.")
        sys.exit()
