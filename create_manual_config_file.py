'''create_manual_config_file.py.

Create config file for twitter extraction based on the manually added names.
'''

import os
import yaml
import pandas as pd

# Input parameters
input_filename = 'sg_manual_names.csv'
input_dir = 'places-info'
input_filepath = os.path.join(input_dir, input_filename)
output_dir = 'config'
output_filename = 'manual_names_config.yaml'
output_filepath = os.path.join(output_dir, output_filename)


def to_lower(text):
    '''helper function to lower case text.'''
    return text.strip().lower()

# read the data
places_data = pd.read_csv(input_filepath)

# filter rows
places_data = places_data[places_data['active'] == 1]
places_data['name'] = places_data['name'].apply(to_lower)
places_data['key'] = places_data['key'].apply(to_lower)

# create config dictionary
config_dict = {}
for _, row in places_data.iterrows():
    place_name = row['name']
    place_key = row['key']
    if place_name not in config_dict:  # first entry
        config_dict[place_name] = {'keywords': []}
    config_dict[place_name]['keywords'] += [place_key]

print '# of places: ', len(config_dict)

# write output file
with open(output_filepath, 'w') as outfile:
    yaml.dump(config_dict, outfile, default_flow_style=False)
