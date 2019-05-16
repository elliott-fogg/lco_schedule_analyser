import dash_html_components as html
from dash_html_components import Strong, Em
import json

# TODO: Refactor this so it works by checking the contents of each object passed
# to it, rather than the value of each object passed to it. This will allow for
# writing final key:value pairs on one line, instead of having to pass them as
# a string. Will also get around the need for an outer-list of numbers.

# TODO: Get divs to start open

# def dict_to_collapsible(input_object):
#     return extract_layer(input_object)
#
# def extract_layer(input_object,indents=0):
#
#     indent_text = str(2*indents) + "em"
#
#     if isinstance(input_object,dict):
#         html_div = html.Div([
#             html.Details([
#                 html.Summary(" "*indents + str(key_value)),
#                 extract_layer(input_object[key_value],indents+1)
#             ]) for key_value in sorted(input_object.keys()) ],
#             style={'text-indent':indent_text}
#         )
#
#     elif isinstance(input_object,list):
#         html_div = html.Div([
#             html.Details([
#                 html.Summary(" "*indents + str(i)),
#                 extract_layer(input_object[i],indents+1)
#             ]) for i in range(len(input_object)) ],
#             style={'text-indent':indent_text}
#         )
#
#     else:
#         # Value is a string (or string-like)
#         try:
#             string_value = str(input_object)
#         except:
#             string_value = "ERROR"
#         html_div = html.Div([
#             html.P(" "*indents + string_value)],
#             style={'text-indent':indent_text}
#         )
#
#     return html_div

def dict_to_collapsible(input_object):
    content_list = []
    if isinstance(input_object,list):
        for item in input_object:
            content_list.append(extract_layer(item))
    elif isinstance(input_object,dict):
        return extract_layer(input_object)
        for key,value in input_object.viewitems():
            content_list.append(
                html.Details([
                    # html.Summary("*{}*:".format(key)),
                    html.Summary([Em(Strong("{}".format(key)))]),
                    extract_layer(value,2)
                ])
            )
    else:
        try:
            string_value = str(input_object)
        except:
            string_value = "!!!ERROR!!!"
        content_list = [html.P(string_value)]

    html_div = html.Div(content_list)
    return html_div

def extract_layer(input_object,indents=0):

    indent_text = str(2*indents) + "em"

    if isinstance(input_object,list):
        # Transform to dict and then continue
        input_object = dict(enumerate(input_object))
    if isinstance(input_object,dict):
        content_list = []
        for key,value in input_object.viewitems():
            if isinstance(value,dict) or isinstance(value,list):
                content_list.append(
                    html.Details([
                        html.Summary(Em(Strong(str(key)))),
                        extract_layer(value,indents+1)
                    ])
                )
            else:
                try:
                    string_value = [Strong(str(key)),": {}".format(value)]
                except:
                    string_value = "!ERROR!"

                content_list.append( html.P(string_value) )
    else:
        # ERROR: Something has gone wrong here. Only Dicts/lists should be passed
        # to this file.
        content_list = [html.P("!!Error!! Not list or dict: {}".format(type(input_object)))]

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

if __name__ == "__main__":
    print extract_layer(test_dict)
