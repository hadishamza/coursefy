# -*- coding: utf-8 -*-
import json
from pprint import pprint

# FILTERS

# Remove empty rows
def filter_empty(json_data):
    output = []
    for row in json_data:
        if row['code'] != '':
            output.append(row)
    return output

def group_by_peroid(json_data):
    output = {}
    period = None
    for row in json_data:
        if row['period'] != '' and row['period'] != None:
            period = row['period']

        output.setdefault(period, []).append(row)
    return output


# Eat kimono-JSON and spit clean usable JSON
with open("it1415.json") as json_file:
    json_data = json.load(json_file)
    #filtered_data = filter_empty(json_data['collection1'])
    filtered_data = group_by_peroid(json_data)
    pprint(filtered_data)

