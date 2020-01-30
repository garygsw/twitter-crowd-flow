'''generate_manual_coords.py.

Generate a table of manual added places infomation table.
'''

import sys
import yaml
import requests
import codecs
import json
import numpy as np


# Input parameters:
input_yaml_file = 'config/manual_places.yaml'
output_file = 'places-info/sg_manual_names.csv'
header_list = ['name', 'key', 'active', 'latitude', 'longitude']
delimiter = ','
header = delimiter.join(header_list)
output_row = '\n' + delimiter.join(['%s'] * len(header_list))
api_key = 'AIzaSyAKuNX8e4RUZs6ecBIbix9duGwK4imVwic'
url_fmt = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'

# read input file
with open(input_yaml_file) as config_file:
    all_place_config = yaml.load(config_file)


# create output file
output_file = codecs.open(output_file, 'w+', 'utf-8')
output_file.write(header)
for place_name, place_config in all_place_config.iteritems():
    if 'keywords' in place_config:
        keywords = place_config['keywords']
        for i, k in enumerate(keywords):
            if i == 0:  # first one`only
                urlk = k.replace(' ', '+')
                url = url_fmt % (urlk, api_key)
                results = requests.get(url)
                results = json.loads(results.text)
                if results['status'] == 'ZERO_RESULTS':  # can't be found
                    lat = np.nan
                    lon = np.nan
                    print k, 'not lat lon'
                else:
                    try:
                        results = results['results'][0]
                        lat = results['geometry']['location']['lat']
                        lon = results['geometry']['location']['lng']
                    except Exception as e:
                        print results
                        sys.exit()
            active = 'active' not in place_config
            active = 1 if active else 0
            values = (place_name, k, active, lat, lon)
            output_values = output_row % values
            output_file.write(output_values)

output_file.close()
