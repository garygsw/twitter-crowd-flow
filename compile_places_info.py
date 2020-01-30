'''compile_places_info.py.

Compile the places latitude and longitudes.
'''

import os
import math
import pandas as pd

# Input parameters
read_list = ['sg_factual_places', 'sg_manual_names', 'sg_mrt_names']
input_dir = 'places-info'
output_dir = 'places-info'
output_filename = 'combined_places_info.csv'
output_path = os.path.join(output_dir, output_filename)


# Grid information - from road network data prepration
Y, X = 54, 90 #46, 87  # 500m grid
max_long, min_long = 104.055, 103.61
max_lat, min_lat = 1.47, 1.205
long_diff = max_long - min_long
lat_diff = max_lat - min_lat


def transform_X(longitude):
    '''helper function to transform X into grid.'''
    return int(math.floor((longitude - min_long) / long_diff * (X - 1)))


def transform_Y(latitude):
    '''helper function to transform Y into grid.'''
    return int(math.floor((max_lat - latitude) / lat_diff * (Y - 1)))



# combine the info files
data_list = [pd.read_csv(os.path.join(input_dir, read + '.csv'))
             for read in read_list]
compiled_data = pd.concat(data_list)
compiled_data['name'] = compiled_data['name'].apply(str.lower)
compiled_data = compiled_data[['name', 'latitude', 'longitude']]
compiled_data = compiled_data.drop_duplicates()
compiled_data = compiled_data.dropna()

# add the grid info
compiled_data['x_grid'] = compiled_data['longitude'].apply(transform_X)
compiled_data['y_grid'] = compiled_data['latitude'].apply(transform_Y)

compiled_data.to_csv(output_path, index=False)
