import dash_html_components as html
from dash_html_components import Strong, Em
import json

def dict_to_collapsible(input_object):
    content_list = []
    if isinstance(input_object,list):
        for item in input_object:
            content_list.append(extract_layer(item))
    elif isinstance(input_object,dict):
        return extract_layer(input_object)
    else:
        try:
            string_value = str(input_object)
        except:
            string_value = "!ERROR! - Non-dict object could not become String" +\
                " - Type = {}".format(type(input_object))
        content_list = [html.P(string_value)]

    html_div = html.Div(content_list)
    return html_div


def extract_layer(input_object,indents=0):
    indent_text = str(2*indents) + "em"
    open_on_default = True

    if isinstance(input_object,list):
        # Transform to dict and then continue
        input_object = dict(enumerate(input_object))
        open_on_default = False

    if isinstance(input_object,dict):
        content_list = []
        for key,value in input_object.viewitems():
            if isinstance(value,dict) or isinstance(value,list):
                content_list.append(
                    html.Details([
                        html.Summary(Em(Strong(str(key)))),
                        extract_layer(value,indents+1)
                    ],open=open_on_default)
                )
            else:
                try:
                    string_value = [Strong(str(key)),": {}".format(value)]
                except:
                    string_value = "!ERROR! - Non-dict object could not " +\
                        "become String - Type = {}".format(type(input_object))

                content_list.append( html.P(string_value) )
    else:
        # ERROR: Something has gone wrong here. Only Dicts/lists should be passed
        # to this file.
        content_list = [html.P("!Error! Not list or dict: {}".format(\
            type(input_object)))]

    html_div = html.Div(content_list,style={'text-indent':indent_text})
    return html_div

test_dict = {
    "outer_layer1": {
        "middle_layer1.1": {
            "inner_layer1.1.1": "inner_value1.1.1",
            "inner_layer1.1.2": "inner_value1.1.2"
            },
        "middle_layer1.2": "middle_value1.2",
        "middle_layer1.3": [
            "list_value1",
            "list_value2",
            "list_value3",
            {
                "dict_in_list1": "value1.3.1",
                "dict_in_list2": {
                    "some_key": "help"
                }
            }
        ]
    }
}

################################################################################

if __name__ == "__main__":
    print extract_layer(test_dict)
