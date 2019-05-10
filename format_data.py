import json, pandas

# Obtain data from the scheduler output
filename = "normal_schedule_20190416024632.json"
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
    r_id = x['request_id']
    r_start = str(x['start']).split("T")
    r_sd = r_start[0]
    r_st = r_start[1]
    r_end = str(x['end']).split("T")
    r_ed = r_end[0]
    r_et = r_end[1]
    return (r_id,r_sd,r_st,r_ed,r_et)

scheduled_requests = [ format_block(x) for x in telescope_info['reservations']]

# Split up any requests that occur over midnight
requests = []
split_requests = []
for req in scheduled_requests:
    if req[1] != req[3]:
        split_requests.append(req)
    else:
        requests.append(req)

for r in split_requests:
    requests.append( r[:3] + (r[1], '23:59:59') )
    requests.append( (r[0], r[3], '00:00:00', r[3], r[4]) )


# Obtain data from the input requests
data = json.load(open("input_request_data.json","r"))
available_telescopes = data['available_resources']
semester_details = data['semester_details']

request_groups = data['json_request_group_list']

def format_request(r):
    ipp = 0






ffd = [ x for x in scheduled_requests if (x[1] == '2019-04-17' or x[3] == '2019-04-17')]

df = [dict(Task=1,Start=x[1]+" "+x[2],Finish=x[3]+" "+x[4]) for x in requests]
