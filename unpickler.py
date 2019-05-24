import pickle, sys, io, contextlib, json, os

cwd = os.getcwd()
pickled_file = "data/scheduling_input_20190416024630.pickle"
json_output_file = "data/input_request_data.json"
adaptive_scheduler_directory = cwd + "/../lco_repos/adaptive_scheduler"

def load_pickled_file():
    """
    Loads the pickled input file.
    """

    cwd = os.getcwd()
    sys.path.insert(0, adaptive_scheduler_directory)
    import adaptive_scheduler
    objects = []
    with open(pickled_file,"rb") as openfile:
        while True:
            try:
                objects.append(pickle.load(openfile))
            except EOFError:
                break
            except Exception as e:
                print "TRIGGERED"
                print e
                return e

    data = objects[0]
    return data

##### Additional Functions #####################################################
# Functions for exporting the unpickled file into plain-text json, so that it
# can be examined in an online JSON viewer, or for loading the unpickled file
# into explorable variables in IPython.

class convert_classes_to_text():
    """
    Converts all custom classes in a dict to strings so that it can be dumped
    into a JSON file.
    """
    nt = 0

    def __init__(self,input_json):
        self.output = self.extract_layer(input_json)

    def extract_layer(self, input_value):
        if isinstance(input_value, dict):
            output_value = {}
            for key in input_value:
                # print "KEY: {}".format(key)
                output_value[str(key)] = self.extract_layer(input_value[key])
        elif isinstance(input_value, list):
            # print "LIST"
            output_value = []
            for item in input_value:
                output_value.append(self.extract_layer(item))
        else:
            # print "STATIC"
            success, output_value = self.make_string(input_value)
            if not success:
                print "untextable_{}: {}".format(self.nt, input_value)
                output_value = "UNTEXTABLE_{}".format(self.nt)
                self.nt += 1
        return output_value

    @staticmethod
    def make_string(input_value):
        try:
            output_value = str(input_value)
            success = True
        except ValueError:
            output_value = None
            success = False
        return success, output_value

def save_json_output(input_json):
    textified = convert_classes_to_text(input_json)
    with open(json_output_file,"w+") as fw:
        fw.write(json.dumps(textified.output))

def load_input(output):
    """
    Loads selections of the unpickled data into variables to play with in IPython.

    data: The whole dict;
    jj: All requests groups in the data;
    jje: An example single request group;
    jjer: The list of requests from the example request group;
    """
    global data, jj, jje, jjer

    try:
        data = output
        jj = data["json_request_group_list"] # total json requests from data
        jje = jj[0] # an example request entry
        jjer = jje["requests"][0] # the request information from the entry
    except Exception as e:
        return e
    return True

##### Silencing Terminal Errors ################################################
# When unpickling the file, because of some classes that are required to
# open it, the terminal throws up some error messages that don't stop the file
# from being loaded. The following functions and classes are to be used to wrap
# the main function to silence these error messages. Plus it's my first time
# using wrappers and I wanted to keep an example.

class DummyFile(object):
    """
    A class that the stdout can be redirected to which will cause writing to do
    nothing. Used for silencing unavoidable warnings and harmless errors.
    """
    def write(self,x): pass
    def flush(self): pass

@contextlib.contextmanager
def silencer(errors=False):
    """
    A wrapper function that silences stdout messages (and stderr messages as
    well passed True as a parameter) for the duration of a function.
    """
    save_stdout = sys.stdout
    if errors:
        save_stderr = sys.stderr
        sys.stderr = DummyFile()
    sys.stdout = DummyFile()
    yield
    sys.stdout = save_stdout
    if errors:
        sys.stderr = save_stderr

def load_pickled_file_quietly():
    with silencer(True):
        data = load_pickled_file()
    return data

################################################################################

if __name__ == "__main__":
    # Check whether we're running in IPython
    try:
        shell = get_ipython()
        # Running in IPython, load unpickled file into memory
        data = load_pickled_file_quietly()
        load_input(data)
    except NameError:
        # Executing script normally, output unpickled json to file, with custom
        # classes having been converted to text so that I can explore it with an
        # online JSON viewer.
        data = load_pickled_file_quietly()
        save_json_output(data)
