import os
import sys
import io
import re

import time

import dateparser
from fuzzywuzzy import process

def is_present(text_list):
    ''' Date parsing and rules to determine whether a text is based in the present '''
    sys.stdout.flush()

    start = time.time()

    results = []

    for text in text_list:
        if len(text) == 0:
            results.append(False)
            continue

        # Filter out future tags
        easy_tags = ["tomorrow", "tmr", "later"]
        hard_tags = ["next week", "next wk", "next month", "next mth", "next year", "next yr", "next time", "this weekend", "at night"]

        easy_extracted = process.extract(text, easy_tags, limit=1)
        hard_extracted = process.extract(text, hard_tags, limit=1)
        # Ratio threshold to exclude tweets
        easy_threshold = 70
        hard_threshold = 90

        # Check if the fuzzy search matches, or if the text contains the exact tag
        if len(easy_extracted) > 0 or any(tag in text for tag in easy_tags):
            # extracted[0] is a tuple, first item text, second item ratio of similarity
            if easy_extracted[0][1] >= easy_threshold:
                results.append(False)
                continue

        if len(hard_extracted) > 0 or any(tag in text for tag in hard_tags):
            if hard_extracted[0][1] >= hard_threshold:
                results.append(False)
                continue

        results.append(True)

    return results

def filter_tweets(tweets, tweet_file, results_filename):
    new_tweets = []
    results = []
    with open(tweet_file, "r") as f:
        new_tweets = f.readlines()
        f.close()
    
    results.append(new_tweets[0]) # Add header

    with open("irrelevant.txt", "a") as f:
        text_list = []
        for i in range(len(tweets)):
            tweet = tweets[i]

            # Convert to ascii
            text = tweet["text"].encode('ascii', 'ignore')
            text_list.append(text)

        tweets_present = is_present(text_list)
        print(len(tweets_present))
        print(len(text_list))

        # Make sure no tweets were removed accidentally
        assert(len(tweets_present) == len(text_list))
        
        for j in range(len(tweets_present)):
            tweet_present = tweets_present[j]
            if not tweet_present:
                # Not relevant
                f.write(text + "\n")
                f.flush()
            else:
                # # Add to results
                with open(results_filename, "a") as nf:
                    nf.write(new_tweets[j+1])
                    nf.flush()
                    nf.close()

                results.append(new_tweets[j+1]) # Add 1 to account for tweet file header

        f.close()

    # print("Percentage of tweets left: {0:3f}".format(float(len(results)) / len(new_tweets)))
    sys.stdout.flush()

    # Write results to file
    with open(results_filename, "w") as f:
        for line in results:
            f.write(line)
        f.close()

    return results

def get_tweets(filename):
    ''' Gets a file name, returns a list of dictionaries for each tweet '''
    tweets = []
    with io.open(filename, "r", encoding="utf-8") as f:
        first_line = f.readline()
        keys = first_line.split(',')

        for line in f:
            split_line = line.strip().split(',')

            # Create a dict for each tweet
            tweet_d = { keys[i].strip() : split_line[i] for i in range(len(keys))}
            tweets.append(tweet_d)

        f.close()

    return tweets


if __name__ == "__main__":
    tweet_set = sys.argv[1]

    total_tweets = 0
    filtered_tweet_count = 0

    tweet_files = os.listdir("tweets/{0}/".format(tweet_set))
    tweet_files = sorted(tweet_files)

    root_path = "../filtered_tweets"
    output_path = "{0}/{1}/".format(root_path, tweet_set)

    if not os.path.isdir(root_path):
        os.mkdir(root_path)

    if not os.path.isdir(output_path):
        os.mkdir(output_path)
    
    for tweet_file in tweet_files:
        full_tweet_filename = "../tweets/{0}/{1}".format(tweet_set, tweet_file)
        full_filtered_filename = "{0}/{1}".format(output_path, tweet_file)

        tweets = get_tweets(full_tweet_filename)
        total_tweets += len(tweets)
        print("Processing {0}: {1} tweets".format(full_tweet_filename, len(tweets)))
        sys.stdout.flush()
    
        # Filter tweets
        filtered_tweets = filter_tweets(tweets, full_tweet_filename, full_filtered_filename)
        filtered_tweet_count += len(filtered_tweets)

    print("Percentage of tweets left: {0:3f}".format(float(filtered_tweet_count) / total_tweets))
