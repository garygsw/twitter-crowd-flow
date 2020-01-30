'''aggregate_tweet_counts.py.

Aggregate the count of tweets per location.
'''

import os
import json
import pandas as pd


# Input parameters
ds_names = ['VDLset1', 'VDLset2', 'VDLset3']
input_dir = 'daily'
places_info_path = 'places-info/combined_places_info.csv'
output_dir = 'agg-tweet-counts'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
output_filename = 'agg_count_%s.json'  # for the datestamp

# Creating timestamp blocks
block_size = 12   # 6 * 5 mins = 30 minutes block
all_timestamps = [''.join([str(hour).zfill(2), str(minute).zfill(2)])
                  for hour in range(24) for minute in range(0, 60, 5)]
timestamps_groups = [all_timestamps[i]
                     for i in range(0, len(all_timestamps), block_size)]

# Read places info
places_info = pd.read_csv(places_info_path, index_col='name')
all_places = list(places_info.index)


def which_timestamp_group(dt):
    '''helper function to find out which timestamp group it belongs.'''
    return dt.replace(minute=0, second=0).strftime('%H%M')

for dataset_name in ds_names:
    # make output paths
    output_path = os.path.join(output_dir, dataset_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    input_path = os.path.join(input_dir, dataset_name)
    input_filenames = os.listdir(input_path)
    for input_file in input_filenames:
        output_dict = {timestamp: {name: 0 for name in all_places}
                       for timestamp in timestamps_groups}
        date = input_file.split('.')[0].split('_')[1]
        output_file = output_filename % date
        output_filepath = os.path.join(output_path, output_file)
        input_filepath = os.path.join(input_path, input_file)
        tweets = pd.read_csv(input_filepath, parse_dates=['date'])
        tweets['time_group'] = tweets['date'].apply(which_timestamp_group)
        time_groups = tweets.groupby(['time_group', 'place'])
        tweet_counts = time_groups.size()
        keys = time_groups.groups.keys()
        for key in keys:
            timestamp, place = key
            if key in tweet_counts.index:
                count = tweet_counts[timestamp][place]
                output_dict[timestamp][place] += count
        with open(output_filepath, 'w') as fp:
            json.dump(output_dict, fp)
