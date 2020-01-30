'''extract_tweets.py.

Extract historical tweets given a time range and a list of keywords.
'''

import os
import re
import codecs
import time
import json
import urllib2
from datetime import datetime
import yaml
from sys import stdout
import got
import socks
import socket
from torrequest import TorRequest


# Input parameters
# format: (name, start date, end date)
# note that start date is 1 day less, and end date is 1 day more, as
# it only starts collection from + 8 hrs of the start day onwards
# and ends collection from +8 hrs of the end day
datasets_details = [
    ('MTCset1test', '2017-07-31', '2017-12-01'),
    ('VLDset1', '2013-02-28', '2013-07-01'),
    ('VLDset2', '2014-08-31', '2015-01-01'),
    ('VLDset3', '2015-11-30', '2016-04-01')
]
config_dir = 'config'
place_group_config = {'mrt-names': 'mrt_stations_names_config.yaml',
                      'factual-places': 'factual_places_config.yaml',
                      'mrt-names': 'manual_names_config.yaml'}
output_path = 'tweets'
if not os.path.isdir(output_path):
    os.mkdir(output_path)
delay = 5    # in between each search API call
header_list = ['username', 'date', 'retweets', 'favorites', 'text', 'geo',
               'mentions', 'hashtags', 'id', 'permalink', 'place', 'key']
delimiter = '\t'
header = delimiter.join(header_list)
csv_row = '\n' + delimiter.join(['%s'] * 2 + ['%d'] * 2 + ['%s'] * 8)
time_format = '%Y-%m-%d %H:%M'
progress_bar_len = 30
time_correction = 8 * 60 * 60
problem_threshold = 0.6
use_tor = True
filter_text = False
reset_identity_interval = 6 * 60 * 60  # 6 hours
progress_bar_text = '\rSaved {} on file: {:.2f}% [{}>{}] - {:.2f}s'


def create_connection(address, timeout=None, source_address=None):
    '''helper function to link socket to tor processs.'''
    sock = socks.socksocket()
    sock.connect(address)
    return sock


def print_progress(place, i, total):
    '''helper function to print progress.'''
    percentage = '%.3f' % (i / float(total) * 100)
    text = 'Extracting {} ({}/{},  {}% completed)'.format(place,
                                                          i,
                                                          total,
                                                          percentage)
    print text


def print_elasped_time(start_time):
    '''helper function to print elasped time.'''
    total_time = time.time() - start_time
    hours = total_time // 3600
    total_time %= 3600
    minutes = total_time // 60
    total_time %= 60
    seconds = total_time
    if hours == 0:
        if minutes == 0:
            print('Time taken: %.2f s' % seconds)
        else:
            print('Time taken: %d mins %.2f s' % (minutes, seconds))
    else:
        print('Time taken: %d hrs %d mins %.2f s' % (hours, minutes, seconds))


def print_current_ip():
    '''helper function to print current ip address.'''
    response = urllib2.urlopen("http://ip.jsontest.com/")
    jsonResponse = response.read()
    data = json.loads(jsonResponse)
    print 'ip address: ', data['ip'], '\n'


def create_regex_list(keyword):
    '''helper function to create a list of regex.'''
    words = keyword.split()
    regex_list = []
    for word in words:
        pattern = r'\b'
        pattern += r'\w*'.join(word)
        pattern += r'\b'
        prog = re.compile(pattern, re.I)
        regex_list.append(prog)
    return regex_list


def main(tr=None):
    '''main function.'''
    overall_start = time.time()
    if tr is not None:
        tor_timer = 0
    tweet_criteria = got.manager.TweetCriteria()
    tweet_criteria.near = '"Central Region, Singapore"'
    grand_total_tweet_count = 0

    for place_set, config_fname in place_group_config.iteritems():
        print 'Reading place config for %s...' % place_set
        config_fpath = os.path.join(config_dir, config_fname)
        with open(config_fpath) as config_file:
            all_places_config = yaml.load(config_file)
        print 'Total place to read: ', len(all_places_config)
        for ds_info in datasets_details:
            ds_start = time.time()
            global ds_total_count
            global current_count
            global percent
            ds_total_count = 0
            problem_places = {}
            ds_name, start_date, end_date = ds_info
            print '\nExtracting for %s...' % ds_name
            output_fpath = os.path.join(output_path, ds_name)
            # create output path
            if not os.path.isdir(output_fpath):
                os.mkdir(output_fpath)
            output_fpath = os.path.join(output_fpath, place_set)
            if not os.path.isdir(output_fpath):
                os.mkdir(output_fpath)
            tweet_criteria.since = start_date
            tweet_criteria.until = end_date
            start_date = datetime.strptime(start_date, '%Y-%m-%d').timetuple()
            start_date = time.mktime(start_date)
            end_date = datetime.strptime(end_date, '%Y-%m-%d').timetuple()
            end_date = time.mktime(end_date)
            duration = end_date - start_date

            i = 0
            total_places = len(all_places_config)
            for place, place_config in all_places_config.iteritems():
                place_start = time.time()
                stdout.write('\n')
                current_count = 0
                output_fname = place + '.csv'
                output_filepath = os.path.join(output_fpath, output_fname)
                if os.path.exists(output_filepath):  # if already exists, ignore
                    print '%s already extracted. skipping...' % place
                    with open(output_filepath) as infile:
                        num_lines = sum(1 for line in infile) - 1
                        print '# of tweets: %d' % num_lines
                        ds_total_count += num_lines
                        i = i + 1
                    continue
                output_file = codecs.open(output_filepath, "w+", "utf-8")
                output_file.write(header)
                percent = 0

                def receive_buffer(tweets):
                    global current_count
                    global percent
                    if filter_text:
                        filtered_tweets = []
                        for t in tweets:
                            if regex_list:
                                search_result = all(bool(prog.search(t.text))
                                                    for prog in regex_list)
                                if search_result:
                                    filtered_tweets.append(t)
                    else:
                        filtered_tweets = tweets
                    total = len(filtered_tweets)
                    current_count += total
                    for t in filtered_tweets:
                        output_file.write((csv_row % (t.username,
                                                    t.date.strftime(time_format),
                                                    t.retweets,
                                                    t.favorites,
                                                    t.text,
                                                    t.geo,
                                                    t.mentions,
                                                    t.hashtags,
                                                    t.id,
                                                    t.permalink,
                                                    place,
                                                    key)))
                    output_file.flush()
                    if current_count >= 0:
                        current_time = time.mktime(t.date.timetuple())
                        current_time -= time_correction
                        diff_time = end_date - current_time
                        percent = diff_time / duration
                        cursor = percent * progress_bar_len
                        cursor = int(cursor)
                        spaces = '.' * (progress_bar_len - cursor)
                        cursor = '=' * cursor
                        elasped_time = time.time() - key_start_time
                        stdout.write(progress_bar_text.format(current_count,
                                                            percent * 100,
                                                            cursor,
                                                            spaces,
                                                            elasped_time))
                        stdout.flush()

                # Set tweet criteria based on type of query
                # This is used for the attribution of the tweet to the particular keyword
                if 'username' in place_config:
                    key = place_config['username']
                    tweet_criteria.username = key
                    if hasattr(tweet_criteria, 'querySearch'):
                        del tweet_criteria.querySearch
                    print_progress(place, i, total_places)
                    print 'using key: ', key
                    regex_list = None
                    key_start_time = time.time()
                    got.manager.TweetManager.getTweets(tweet_criteria,
                                                    receive_buffer)
                    stdout.write('\n')
                else:
                    print_progress(place, i, total_places)
                    all_keywords = place_config['keywords']
                    if hasattr(tweet_criteria, 'username'):
                        del tweet_criteria.username
                    for key in all_keywords:
                        tweet_criteria.querySearch = key
                        print 'using key: ', key
                        regex_list = create_regex_list(key)
                        key_start_time = time.time()
                        got.manager.TweetManager.getTweets(tweet_criteria,
                                                        receive_buffer)
                        if 0 < percent < problem_threshold:
                            problem_places[place] = percent * 100
                        stdout.write('\n')

                output_file.close()
                ds_total_count += current_count
                print_elasped_time(place_start)
                i = i + 1
                time.sleep(delay)
                if tr is not None:
                    time_taken = time.time() - place_start
                    tor_timer += time_taken
                    if tor_timer / reset_identity_interval > 1:
                        stdout.write('\n')
                        tor_timer = 0
                        print 'reseting ip address...'
                        tr.reset_identity()
                        print_current_ip()

            grand_total_tweet_count += ds_total_count
            print_elasped_time(ds_start)
            print '\nTotal tweet count for %s is %d' % (ds_name, ds_total_count)

            if len(problem_places) > 0:
                print '\nPossible problem places:'
                for place, value in problem_places.iteritems():
                    print place, value

    print 'All completed'
    print '\nTotal tweet count is %d' % grand_total_tweet_count
    print_elasped_time(overall_start)

if __name__ == '__main__':
    if use_tor:
        with TorRequest(proxy_port=9050, ctrl_port=9051, password=None) as tr:
            print '\nSetting up Tor service...'
            print_current_ip()
            socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9050)
            socket.socket = socks.socksocket
            socket.create_connection = create_connection
            main(tr)
    else:
        main()
