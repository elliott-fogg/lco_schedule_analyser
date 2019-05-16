import dash_html_components as html
import json

def dict_to_collapsible(input_object):
    return extract_layer(input_object)

def extract_layer(input_object,indents=0):

    indent_text = str(2*indents) + "em"

    if isinstance(input_object,dict):
        html_div = html.Div([
            html.Details([
                html.Summary(" "*indents + str(key_value)),
                extract_layer(input_object[key_value],indents+1)
            ]) for key_value in sorted(input_object.keys()) ],
            style={'text-indent':indent_text}
        )

    elif isinstance(input_object,list):
        html_div = html.Div([
            html.Details([
                html.Summary(" "*indents + str(i)),
                extract_layer(input_object[i],indents+1)
            ]) for i in range(len(input_object)) ],
            style={'text-indent':indent_text}
        )

    else:
        # Value is a string (or string-like)
        try:
            string_value = str(input_object)
        except:
            string_value = "ERROR"
        html_div = html.Div([
            html.P(" "*indents + string_value)],
            style={'text-indent':indent_text}
        )

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
