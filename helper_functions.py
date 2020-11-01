"""
These two functions help take twitter data and turn it into a
workable corpus for NLP
"""

import pandas as pd
import numpy as np
import pickle
import json


def txt_to_df(txt_path):
    """
    Powerhouse function to take raw scraped twitter data
    into a DataFrame of just the tweet texts

    Args:
        txt_path: The path for the saved file containing
            the tweet data in json format
    
    Returns:
        A DataFrame containing just the raw tweet texts
    """
    path = txt_path
    tweets_file = open(path, "r")
    tweets_data = []
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    tweet = pd.DataFrame(tweets_data)
    tweet = tweet[tweet["lang"] == "en"]
    tweet = tweet[["text", "truncated", "extended_tweet", "retweeted_status"]]
    tweet["long_text"] = tweet.apply(ext_tweets, axis=1)
    tweet["long_text"] = tweet.apply(ext_rt, axis=1)
    return tweet[["long_text"]]


def ext_tweets(row):
    """
    Helper function to determined truncated tweets and
    then return the full tweet

    Args:
        row: the row a larger DataFrame consisting of all
            tweet information

    Returns:
        A new row with the full tweet text
    """
    if row["truncated"] == True:
        return row["extended_tweet"]["full_text"]
    else:
        return row["text"]


def ext_rt(row):
    try:
        if type(row["retweeted_status"]) == dict:
            return row["retweeted_status"]["extended_tweet"]["full_text"]
        else:
            return row["long_text"]
    except:
        return row["long_text"]

