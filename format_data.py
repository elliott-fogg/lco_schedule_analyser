import json
import pandas as pd
from copy import copy
import unpickler
from datetime import datetime

input_filepath = "sample_files/sample_input.pickle"
output_filepath = "sample_files/sample_output.json"

def read_input_file(filepath):
    # Load the pickled file
    data = unpickler.load_pickled_file(filepath, True)

    request_groups = data['json_request_group_list']

    # Proposal Priorities
    proposals_objects = data['proposals_by_id']
    proposals = { val.id: val.tac_priority for (key,val) in \
        proposals_objects.items()}

    observation_requests = []
    for r_group in request_groups:
        request_base = {key:r_group[key] for key in \
            ['name', 'ipp_value', 'observation_type', 'proposal']}
        request_base['proposal_priority'] = proposals[request_base['proposal']]
        request_base['priority_value'] = request_base['proposal_priority'] * \
            request_base['ipp_value']
        request_base['group_id'] = r_group['id']

        individual_requests = r_group['requests']
        for request in individual_requests:
            request_info = copy(request_base)
            request_info['request_id'] = request['id']
            request_info["acceptability_threshold"] = request['acceptability_threshold']
            request_info['duration'] = request['duration']
            request_info['priority_total'] = request_info['priority_value'] * \
                request_info['duration']

            # Format Window Strings
            windows = []
            for w in request['windows']:
                windows.append("{} -> {}".format(w['start'], w['end']))
            request_info['windows'] = windows

            configurations = []
            for c in request['configurations']:
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
                config['target_name'] = target.name
                config['target_ra'] = target.get_ra().degrees
                config['target_dec'] = target.get_dec().degrees
                # Input instrument configurations as JSON text blocks
                config['instrument_configs'] = c['instrument_configs']
                configurations.append(config)

            request_info['configurations'] = configurations
            observation_requests.append(request_info)
    return observation_requests


# Get all relevant information from the Scheduler Output
def read_output_file(filepath):
    if not filepath.endswith(".json"):
        print("ERROR: File is not of type .json: '{}'".format(filepath))
        return None

    data = unpickler.load_json_file(filepath)

    scheduled_requests = []
    for telescope in data['resources']:
        for r in data['resources'][telescope]['reservations']:

            r_dict = {}
            r_dict['telescope'] = telescope
            start_dt = datetime.strptime(r['start'], "%Y-%m-%dT%H:%M:%S")
            end_dt = datetime.strptime(r['end'], "%Y-%m-%dT%H:%M:%S")

            r_dict['id'] = r['request_id']

            r_dict['start_string'] = start_dt.strftime("%Y-%m-%d %H:%M:%S")
            r_dict['end_string'] = end_dt.strftime("%Y-%m-%d %H:%M:%S")

            r_dict['start_time'] = start_dt.strftime("%H:%M:%S")
            r_dict['end_time'] = end_dt.strftime("%H:%M:%S")

            r_dict['start_date'] = start_dt.strftime("%Y-%m-%d")
            r_dict['end_date'] = end_dt.strftime("%Y-%m-%d")

            scheduled_requests.append(r_dict)

    return scheduled_requests


# Compile all information into a dataframe to be used by Plotly
def obtain_dataframe(input_file=input_filepath, output_file=output_filepath):
    requests_df = pd.DataFrame(read_input_file(input_file))
    scheduled_df = pd.DataFrame(read_output_file(output_file))

    df = requests_df.join(scheduled_df.set_index('id'), on='request_id')

    df['scheduled'] = df['start_date'].notnull()

    return df


################################################################################
