'''create_tweet_counts_h5.py.

Creates the tweet count matrixes in the required format of .h5.
'''

import os
import time
import h5py
import numpy as np


# Input parameters
ds_names = ['VLDset1', 'VLDset2', 'VLDset3']
w, h = 89, 49  # 87, 46  # for 500m, (44, 23) for 1km
grid = 'M{}x{}'.format(w, h)
input_dir = 'grid-tweet-counts/%s/%s'  # for ds name and grid
output_dir = 'dataset'
if not os.path.isdir(output_dir):
    os.mkdir(output_dir)
h5_filename_format = 'SG_%s_M%sx%s_T%s_TweetCount-%s+%s.h5'  # name, w, h, interval, lag
block_size = 6   # 6 * 5 mins = 30 minutes block
block_time = block_size * 5
lags = 1
leads = 10

for ds_name in ds_names:
    print 'reading ' + ds_name + '...'
    ts = time.time()
    output_path = os.path.join(output_dir, h5_filename_format)
    h5_filename = output_path % (ds_name, w, h, block_time, lags, leads)
    f = h5py.File(h5_filename, 'w')

    # Create the date dataset
    # a list of timestamps associate with the data
    count_fnames = os.listdir(input_dir % (ds_name, grid))
    count_fnames = sorted(count_fnames)
    start_index = (24 * 60 / block_time) - lags
    end_index = - (24 * 60 / block_time) + leads
    count_fnames = count_fnames[start_index:end_index]
    all_datetimeslots = [x[-17:-4] for x in count_fnames]
    date_dataset = f.create_dataset("date", data=np.array(all_datetimeslots))

    # Create the tweet count dataset
    # a 3D tensor of shape (number_of_timeslots, h, w),
    # of which data[i] is a 2D tensor of shape (h, w) containing the flow count
    number_of_timeslots = len(all_datetimeslots)
    count_data = []
    for count_fname in count_fnames:
        data = np.load(os.path.join(input_dir, count_fname) % (ds_name, grid))
        count_data.append(data)
    flow_dataset = f.create_dataset("count", data=np.array(count_data))

    f.close()
    print 'Elapsed time (loading data): %.3f seconds\n' % (time.time() - ts)
