import pickle, sys, io, contextlib, json, os

pickled_file = "/home/foggy/Documents/repos/data/scheduling_input_20190416024630.pickle"
json_output_file = "/home/foggy/Documents/repos/data/input_request_data.json"
adaptive_scheduler_directory = "/home/foggy/Documents/repos/adaptive_scheduler"

def load_pickled_file():
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

class unpack_json():
    nt = 0

    def __init__(self,input_json):
        unpacked = self.unpack(input_json)
        self.output = unpacked

    def unpack(self, input_json):
        output_json = self.extract_layer(input_json)
        return output_json

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
    unpacked = unpack_json(input_json)
    with open(json_output_file,"w+") as fw:
        fw.write(json.dumps(unpacked.output))

def load_input(output):
    global data, jj, jje, jjer

    try:
        data = output
        jj = data["json_request_group_list"] # total json requests from data
        jje = jj[0] # an example request entry
        jjer = jje["requests"][0] # the request information from the entry
    except Exception as e:
        return e
    return True

class DummyFile(object):
    def write(self,x): pass
    def flush(self): pass

@contextlib.contextmanager
def silencer(errors=False):
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

if __name__ == "__main__":
    # Unpickle file
    data = load_pickled_file()
    # Check whether we're running in IPython
    try:
        shell = get_ipython()
        print sys.stdout
        # Running in IPython, load variables
        with silencer(True):
            data = load_pickled_file()
        load_input(data)
    except NameError:
        # Executing script normally, output unpickled json to file
        with silencer():
            data = load_pickled_file()

        save_json_output(data)
