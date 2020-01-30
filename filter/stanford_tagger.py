import os
import sys
import copy
import io
from nltk.parse import stanford

import time

os.environ['STANFORD_PARSER'] = 'models/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'models/stanford-parser-3.8.0-models.jar'

def is_present(parser, text_list):
    ''' Use constituency parsing to see whether tense of a sentence is present '''

    # Determine tags for each tense
    past_tags = ("VBD", "VBN")
    present_tags = ("VBG", "VBZ", "VBP")
    future_tags = ("MD")

    print("{0} sentences to parse.".format(len(text_list)))
    sys.stdout.flush()

    start = time.time()
    sentences_list = list(parser.raw_parse_sents(text_list))

    print("Time taken to parse: {0:5f}s".format(time.time() - start))
    sys.stdout.flush()

    results = []

    for i in range(len(sentences_list)):
        # Store count of each tag
        count = {"past": 0, "present": 0, "future": 0}

        sentences = sentences_list[i]
        node = sentences.next() # Since there is only one sentence, this will return the parent node

        all_VPs = list(node.subtrees(filter=lambda x : x.label() == "VP"))

        # Unknown tense, assume it is present
        if len(all_VPs) == 0:
            results.append(True)
        else:
            # Known tense
            # Get all outermost verbs
            first_VP = all_VPs[0]
            VP_pos = first_VP.pos()

            for word, tag in VP_pos:
                if tag in past_tags:
                    count["past"] += 1
                elif tag in present_tags:
                    count["present"] += 1
                elif tag in future_tags:
                    count["future"] += 1

            # Be more conservative, return false if either future or past is >=, and true o.w.
            if count["past"] >= count["present"] or count["future"] >= count["present"]:
                results.append(False)
            else:
                results.append(True)

    return results

def filter_tweets(tweets, tweet_file, results_filename):
    new_tweets = []
    results = []
    with open(tweet_file, "r") as f:
        new_tweets = f.readlines()
        f.close()
    
    results.append(new_tweets[0]) # Add header

    parser = stanford.StanfordParser(model_path="models/englishPCFG.ser.gz")

    with open("irrelevant.txt", "a") as f:
        # results = copy.deepcopy(tweets)
        text_list = []
        for i in range(len(tweets)):
            tweet = tweets[i]

            # Convert to ascii
            text = tweet["text"].encode('ascii', 'ignore')
            text_list.append(text)

        tweets_present = is_present(parser, text_list)
        
        for i in range(len(tweets_present)):
            tweet_present = tweets_present[i]
            if not tweet_present:
                # Not relevant
                f.write(text + "\n")
                f.flush()
            else:
                # # Add to results
                with open(results_filename, "a") as nf:
                    nf.write(new_tweets[i+1])
                    nf.flush()
                    nf.close()

                results.append(new_tweets[i+1]) # Add 1 to account for tweet file header

        f.close()

    print("Percentage of tweets left: {0:3f}".format(float(len(results)) / len(new_tweets)))
    sys.stdout.flush()

    # Write results to file
    with open(results_filename + ".final", "w") as f:
        for line in results:
            f.write(line)
        f.close()

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
    root_dir = "../filtered_tweets"
    tweet_set = sys.argv[1]
    tweet_file = sys.argv[2]
    
    full_tweet_filename = "../tweets/{0}/{1}".format(tweet_set, tweet_file)
    full_filtered_filename = "../filtered_tweets/{0}/{1}".format(tweet_set, tweet_file)
    print("Processing {0}".format(full_tweet_filename))
    sys.stdout.flush()

    tweets = get_tweets(full_tweet_filename)
    
    # Filter tweets
    filtered_tweets = filter_tweets(tweets, full_tweet_filename, full_filtered_filename)

