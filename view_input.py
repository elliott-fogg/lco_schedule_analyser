import json
import pickle
import pandas as pd
import numpy as np
import matplotlib
from unpickler import load_pickled_file

def get_input_data(input_filepath):
    with open(input_filepath, "r") as openfile:
        data = json.load(openfile)

    # Overview information
    available_telescopes = data['available_resources']
    semester_details = data['semester_details']

    # Proposal Priorities
    proposals_objects = data['proposals_by_id']

    proposals = { val["id"]: val["tac_priority"] for (key,val) in \
        proposals_objects.items()}

    # Schedule Parameters?
    ## Not really necessary information, I think. Can add later if desired.

    # Request Data
    request_groups = data['json_request_group_list']
    observation_requests = []
    for request in request_groups:
        r = {}
        r['request_name'] = request['name']
        r['ipp'] = request['ipp_value']
        r['request_type'] = request['observation_type']
        r['proposal_name'] = request['proposal']
        r['proposal_priority'] = proposals[r['proposal_name']]
        r['priority_value'] = float(r['proposal_priority']) * float(r['ipp'])
        r['request_id'] = request['id']
        r['telescope_class'] = request["location"]["telescope_class"]

        # Observation Details
        individual_requests = request['requests']
            # NOTE:
            # Observation groups in the current dataset only have 1 request each
            # Thus the information for that request has been taken to represent
            # the entire 'group'.
            # This will have to change for cadenced observations.
        if len(individual_requests) > 1:
            print("WARNING: This observation request group has more than one "+\
                "request inside.\nSoftware needs to be redesigned for "+\
                "multi-request groups.")

        details = individual_requests[0]
        r['acceptability_threshold'] = details['acceptability_threshold']
        r['duration'] = details['duration']
        # r['observation_id'] = details['id']
        r['priority_total'] = float(r['priority_value']) * float(r['duration'])

        # Format Window strings
        windows = []
        for w in details['windows']:
            windows.append(
                "{} -> {}".format(
                    " ".join(w['start'][:-1].split("T")),
                    " ".join(w['end'][:-1].split("T"))
                )
            )
        r['windows'] = windows

        # Configuration Details
        configurations = []
        for c in details['configurations']:
            config = {}
            config['acquisition_mode'] = c['acquisition_config']['mode']
            config['max_airmass'] = c['constraints']['max_airmass']
            config['min_lunar_distance'] = c['constraints']['min_lunar_distance']
            config['guiding'] = c['guiding_config']['mode']
            config['subrequest_id'] = c['id']
            config['instrument_type'] = c['instrument_type']
            config['config_priority'] = c['priority']
            # Target Information
            target = c['target']
            config['target_name'] = target['name']
            # config['target_ra'] = target.get_ra().degrees
            # config['target_dec'] = target.get_dec().degrees
            config["target_ra"] = target["_ra"]
            config["target_dec"] = target["_dec"]
            # Input instrument configurations as JSON text blocks
            config['instrument_configs'] = c['instrument_configs']
            configurations.append(config)
        r['configurations'] = configurations

        observation_requests.append(r)

    return observation_requests


def obtain_dataframe(observation_requests):
	requests_df = pd.DataFrame(observation_requests)
	requests_df["request_id"] = requests_df["request_id"].astype(int)

	return requests_df

# # Compile all information into a dataframe to be used by Plotly
# def obtain_dataframe():
#     requests_df = pd.DataFrame(get_input_data())
#     requests_df = requests_df.astype({"request_id": "int32"})
#     scheduled_df = pd.DataFrame(get_output_data())

#     print(requests_df.columns)
#     print(requests_df.dtypes)
#     print(scheduled_df.columns)
#     print(scheduled_df.dtypes)

#     df = requests_df.join(scheduled_df.set_index('id'), on='request_id')

#     df['scheduled'] = df['start'].notnull()

#     return df

#####

if __name__ == "__main__":
	default_file = "sample_files/sample_input.json"
	requests_df = pd.DataFrame(get_input_data(default_file))
	print(requests_df)
