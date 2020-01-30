'''create_tweet_grid_counts.py.

Create the tweet grid count matrix.
'''

import os
import json
import numpy as np
import pandas as pd

# Input parameters
ds_names = ['VLDset1', 'VLDset2', 'VLDset3']
w, h = 89, 49  # for 500m, (44, 23) for 1km    # should i expand the w and h?
grid = 'M{}x{}'.format(w, h)
input_dir = 'agg-tweet-counts'
places_info_path = 'places-info/combined_places_info.csv'
output_dir = 'grid-tweet-counts'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
output_filename = 'tweetcount_%s_%s.npy'  # for date and time


# Read places info
places_info = pd.read_csv(places_info_path, index_col='name')
all_places = list(places_info.index)


for ds_name in ds_names:
    # Create output dir if not present
    output_path = os.path.join(output_dir, ds_name)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    output_path = os.path.join(output_path, grid)
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    input_path = os.path.join(input_dir, ds_name)
    agg_count_fnames = os.listdir(input_path)
    for filename in agg_count_fnames:
        print 'reading ', filename, '...'
        date = filename.split('.')[0].split('_')[-1]
        input_filepath = os.path.join(input_path, filename)
        js = open(input_filepath).read()
        data = json.loads(js)

        for timestamp in data:
            output_file = output_filename % (date, timestamp)
            if os.path.exists(output_file):
                continue
            output = np.zeros((h, w), dtype=np.float64)
            for place in all_places:
                if place not in data[timestamp]:  # eid not in this cv set
                    continue
                y = places_info.at[place, 'y_grid']
                x = places_info.at[place, 'x_grid']
                if x >= w or y >= h:
                    print place, 'out of bounds...', x, y
                    # mostly sentosa places
                    # resorts world sentosa out of bounds... 44 46       - add 1 to h down
                    # siloso beach out of bounds... 42 46                - add 1 to h down                    # madame tussauds singapore out of bounds... 43 46   - add 1 to h
                    # palawan beach out of bounds... 44 47               - add 2 to h down
                    # tanjong beach out of bounds... 45 48               - add 3 to h down
                    # festive grand theatre out of bounds... 45 47       - add 2 to h down
                    # changi exhibition centre out of bounds... 88 22    - add 2 to w right
                    # wave house sentosa out of bounds... 42 46          - add 1 to h down
                    # universal studios singapore out of bounds... 43 46 - add 1 to h down
                    # tanjong beach club out of bounds... 45 48          - add 3 to h down
                    continue
                output[y][x] += data[timestamp][place]

            # save the array
            output_filepath = os.path.join(output_path, output_file)
            np.save(output_filepath, output)
