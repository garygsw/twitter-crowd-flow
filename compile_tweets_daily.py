'''compile_tweets_daily.py.

Compile the tweets into daily files.
'''

import os
import time
import csv
import pandas as pd
from datetime import datetime

# note: add 1 day to the end for filtering purposes &
#       add 1 more day at the end for lead data
#       minus 1 day for predictive purposes
datasets_details = [
    ('VLDset1', '2013-02-28', '2013-07-02'),
    ('VLDset2', '2014-08-31', '2015-01-02'),
    ('VLDset3', '2015-11-30', '2016-04-02')
]
input_path = 'tweets'
output_path = 'daily'
read_list = ['factual-places', 'manual-places', 'mrt-names']

dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M')
overall_start = time.time()

for ds_info in datasets_details:
    ds_name, start_date, end_date = ds_info
    print 'reading ' + ds_name + ' now...'
    output_dir = os.path.join(output_path, ds_name)
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for read in read_list:
        input_dir = os.path.join(input_path, ds_name, read)
        topic_fnames = os.listdir(input_dir)
        data_list = [pd.read_csv(input_dir + '/' + topic_fname, sep='\t', parse_dates=['date'],
                                 date_parser=dateparse, warn_bad_lines=True, error_bad_lines=False,
                                 quoting=csv.QUOTE_NONE, encoding='utf-8')
                     for topic_fname in topic_fnames
                     if topic_fname[0] != '.']
        compiled_data = pd.concat(data_list)

    # filter dates to be in between start and end date
    compiled_data = compiled_data.drop_duplicates(subset=['id'])
    compiled_data = compiled_data[(compiled_data['date'] >= start_date) & (compiled_data['date'] < end_date)]
    compiled_data = compiled_data.sort_values(by='date')
    date_groups = compiled_data.groupby(compiled_data['date'].map(lambda x: (x.year, x.month, x.day)))
    data_groups = [(group, date_groups.get_group(group)) for group in date_groups.groups]
    for date, data in data_groups:
        datex = datetime(year=date[0], month=date[1], day=date[2])
        outputFileName = output_dir + '/tweets_%s.csv' % datex.strftime('%Y%m%d')
        data.to_csv(outputFileName, index=False, encoding='utf8')

print('All completed')
print("\nTotal elapsed time: %.3f seconds\n" % (time.time() - overall_start))
