'''create_mrt_config_file.py.

Create config file for twitter extraction based on the mrt stations names.
'''

import os
import yaml
import pandas as pd

# Input parameters
input_filename = 'sg_mrt_names.csv'
input_dir = 'places-info'
input_filepath = os.path.join(input_dir, input_filename)
output_dir = 'config'
output_filename = 'mrt_stations_names_config.yaml'
output_filepath = os.path.join(output_dir, output_filename)
selected_lines = ['North-South',
                  'East-West',
                  'North-East',
                  'Downtown',
                  'Circle',
                  'Thomson-East']


def to_lower(text):
    '''helper function to lower case text.'''
    return text.strip().lower()


def is_part_of_line(lines):
    '''helper function to filter selected lines.'''
    for line in selected_lines:
        if line in lines:
            return True
    else:
        return False


# read the data
mrt_data = pd.read_csv(input_filepath)

# filter rows
mrt_data = mrt_data[mrt_data['line'].apply(is_part_of_line)]
mrt_data = mrt_data[mrt_data['active'] == 1]
mrt_data['name'] = mrt_data['name'].apply(to_lower)
mrt_data['key'] = mrt_data['key'].apply(to_lower)

# create config dictionary
config_dict = {}
for _, row in mrt_data.iterrows():
    place_name = row['name']
    place_key = row['key']
    if place_name not in config_dict:  # first entry
        config_dict[place_name] = {'keywords': []}
    config_dict[place_name]['keywords'] += [place_key]

print '# of places: ', len(config_dict)

# write output file
with open(output_filepath, 'w') as outfile:
    yaml.dump(config_dict, outfile, default_flow_style=False)
