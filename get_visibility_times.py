import requests, os, json, datetime
from format_data import obtain_dataframe

vis_file_path = "../data/visibilities.json"

def get_visibilities(df):
    if os.path.isfile(vis_file_path):
        print "Visibilities file already exists"
        # Add option to update, or option to select based on schedule
        return

    visibilities = {}
    headers = {"Authorization": request_data['authentication']}
    for request_id in df['request_id']:
        url = request_data['url'].format(request_id)
        r = requests.get(url=url,headers=headers)
        if r.status_code != 200:
            print "Error: Failed connection. Status_code: {}".format(r.status_code)
            continue
        data = r.json()
        visible_times = data['airmass_data']['sor']['times']
        visibilities[request_id] = visible_times

    json.dump(visibilities,open(vis_file_path,"w+"))

def get_time_from_string(s):
    date = datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M")
    return date

def get_visible_windows():
    vis = json.load(open(vis_file_path,"r"))
    visible_windows = {}
    for request_id in vis:
        vis_start = get_time_from_string(vis[request_id][0])
        vis_end = get_time_from_string(vis[request_id][-1])
        vis_duration = vis_end - vis_start
        print vis_duration.days * 144 + vis_duration.seconds / 60 / 10 + 1, len(vis[request_id])
        for time in vis[request_id]:
            print time
        print ""

if __name__ == '__main__':
    # df = obtain_dataframe()
    # get_visibilities(df)
    get_time_from_string('2019-04-16T09:06')
    get_visible_windows()
