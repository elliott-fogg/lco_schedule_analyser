import json, os
import pandas as pd

input_filepath = os.getcwd() + "/../data_files/.json"
output_filepath = os.getcwd() + "/../data_files/sample_output.json"

# Get all relevant information from the Scheduler Output
def get_output_data():
    filename = output_filepath
    with open(filename, "r") as openfile:
        data = json.loads(openfile.read())

    semester_id = data['semester_id']
    schedule_start = data['schedule_start']
    schedule_end = data['schedule_end']
    horizon_days = data['horizon_days']
    total_priority = data['total_priority_value']

    telescope_name = "4m0a.doma.sor"
    telescope_info = data['resources'][telescope_name]
    telescope_priority = telescope_info['priority_value']
    dark_intervals = telescope_info['dark_intervals']

    def format_block(r):
        r_start = str(x['start']).split("T")
        r_finish = str(x['end']).split("T")

        return {
            "id": r['request_id'],
            "start": " ".join(r_start),
            "finish": " ".join(r_finish),
            "start_date": r_start[0],
            "start_time": r_start[1],
            "finish_date": r_finish[0],
            "finish_time": r_finish[1]
        }

    scheduled_reqs = [ format_block(x) for x in telescope_info['reservations']]

    return scheduled_reqs

# Get all relevant information from the Observation Request input
def get_input_data():

    # Load the pickled datafile
    from unpickler import load_pickled_file
    data = load_pickled_file()

    # Overview information
    print("YO", data)
    available_telescopes = data['available_resources']
    semester_details = data['semester_details']

    # Proposal Priorities
    proposals_objects = data['proposals_by_id']
    proposals = { val.id: val.tac_priority for (key,val) in \
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
        r['priority_value'] = r['proposal_priority'] * r['ipp']
        r['request_id'] = request['id']

        # Observation Details
        individual_requests = request['requests']
            # NOTE:
            # Observation groups in the current dataset only have 1 request each
            # Thus the information for that request has been taken to represent
            # the entire 'group'.
            # This will have to change for cadenced observations.
        if len(individual_requests) > 1:
            print "WARNING: This observation request group has more than one "+\
                "request inside.\nSoftware needs to be redesigned for "+\
                "multi-request groups."

        details = individual_requests[0]
        r['acceptability_threshold'] = details['acceptability_threshold']
        r['duration'] = details['duration']
        # r['observation_id'] = details['id']
        r['priority_total'] = r['priority_value'] * r['duration']

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
            config['target_name'] = target.name
            config['target_ra'] = target.get_ra().degrees
            config['target_dec'] = target.get_dec().degrees
            # Input instrument configurations as JSON text blocks
            config['instrument_configs'] = c['instrument_configs']
            configurations.append(config)
        r['configurations'] = configurations

        observation_requests.append(r)

    return observation_requests

# Compile all information into a dataframe to be used by Plotly
def obtain_dataframe():
    requests_df = pd.DataFrame(get_input_data())
    scheduled_df = pd.DataFrame(get_output_data())

    df = requests_df.join(scheduled_df.set_index('id'), on='request_id')

    df['scheduled'] = df['start'].notnull()

    return df


################################################################################

if __name__ == "__main__":
    requests = get_output_data()

    df = obtain_dataframe()

    print df.head()
