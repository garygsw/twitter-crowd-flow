'''create_fatual_config_file.py.

Create config file for twitter extraction based on the factual places names.
'''

import os
import yaml
import pandas as pd

# Input parameters
input_filename = 'sg_factual_places.csv'
input_dir = 'places-info'
input_filepath = os.path.join(input_dir, input_filename)
output_dir = 'config'
output_filename = 'factual_places_config.yaml'
output_filepath = os.path.join(output_dir, output_filename)


def to_lower(text):
    '''helper function to lower case text.'''
    return text.strip().lower()


# read the data
factual_data = pd.read_csv(input_filepath)

# create config dictionary
config_dict = {}
for _, row in factual_data.iterrows():
    place_name = row['name']
    if place_name not in config_dict:  # first entry
        config_dict[place_name] = {'keywords': []}
    config_dict[place_name]['keywords'] += [place_name]

print '# of places: ', len(config_dict)

# write output file
with open(output_filepath, 'w') as outfile:
    yaml.dump(config_dict, outfile, default_flow_style=False)
