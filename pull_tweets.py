from tweepy import OAuthHandler
import tweepy
import pandas as pd
import os
import time
from datetime import datetime
from keys import API_KEY, API_SECRET, ACCESS_KEY, ACCESS_TOKEN_SECRET


auth = OAuthHandler(consumer_key=API_KEY, consumer_secret=API_SECRET)
auth.set_access_token(key=ACCESS_KEY, secret=ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def extract_tweets(search_words, date_since, numTweets, numRuns):
    """
    This function pulls 2500 tweets per run based on search words in batches, and saves the tweets after
    every run.

    :param search_words: (String) Words based on which tweets are filtered
    :param date_since: (String) The oldest date for which tweets need to be pulled
    :param numTweets: (int) Number of tweets to be pulled per run
    :param numRuns: (int) Number of runs

    :return: None
    """
    program_start = time.time()

    # Pull tweets in batches to avoid getting denied
    for i in range(0, numRuns):
        # We will time how long it takes to scrape tweets for each run:
        start_run = time.time()
        db_tweets = pd.DataFrame(columns=['username', 'acctdesc', 'location', 'following',
                                          'followers', 'totaltweets', 'usercreatedts', 'tweetcreatedts',
                                          'retweetcount', 'text', 'hashtags']
                                 )
        # Collect tweets using the Cursor object
        tweets = tweepy.Cursor(api.search, q=search_words, lang="en", since=date_since, tweet_mode='extended').items(
            numTweets)  # Store these tweets into a python list
        tweet_list = [tweet for tweet in tweets]  # Obtain the following info (methods to call them out):
        
        n_tweets = 0
        # Pull the values
        for tweet in tweet_list:
            # twitter handle
            username = tweet.user.screen_name
            # description of account
            acctdesc = tweet.user.description
            # where is the user tweeting from
            location = tweet.user.location
            # no. of other users that user is following (following)
            following = tweet.user.friends_count
            # no. of other users who are following this user (followers)
            followers = tweet.user.followers_count
            # total tweets by user
            totaltweets = tweet.user.statuses_count
            # when the user account was created
            usercreatedts = tweet.user.created_at
            # when the tweet was created
            tweetcreatedts = tweet.created_at
            # no. of retweets
            retweetcount = tweet.retweet_count
            # hashtags in the tweet
            hashtags = tweet.entities['hashtags']

            # if it's a retweet, take retweets full text
            try:
                text = tweet.retweeted_status.full_text
            except AttributeError:  # Not a Retweet
                text = tweet.full_text
            # Add the 11 variables to the empty list - ith_tweet:
            ith_tweet = [username, acctdesc, location, following, followers, totaltweets,
                         usercreatedts, tweetcreatedts, retweetcount, text, hashtags]  # Append to dataframe - db_tweets
            db_tweets.loc[len(db_tweets)] = ith_tweet
            n_tweets += 1

        end_run = time.time()
        duration_run = round((end_run - start_run) / 60, 2)

        print('No. of tweets scraped for run {} is {}'.format(i + 1, n_tweets))
        print('Time taken for run {} to complete is {} mins'.format(i + 1, duration_run))
        print('Saving dataframe fragment...')
        to_csv_timestamp = datetime.today().strftime('%Y%m%d_%H%M%S')  # Define working path and filename
        path = os.getcwd()

        # Save output for each run
        filename = path + '/data/' + to_csv_timestamp + '_scraped_tweets_run_%d.csv' % (
                    i + 1)

        # save dataframes from each run separately
        db_tweets.to_csv(filename, index=False)
        # 15 minute sleep time to avoid getting denied by the API
        print('Sleeping for 15 mins...')
        time.sleep(920)

    program_end = time.time()
    print('Scraping has completed!')
    print('Total time taken to scrap is {} minutes.'.format(round(program_end - program_start) / 60, 2))


if __name__ == "__main__":
    search_words = "trump OR biden OR covid OR coronavirus OR mask OR distancing OR vote OR voting OR election OR\
                    vaccine OR virus OR (work from home) OR wfh OR lockdown OR capitol OR (white house) OR (black \
                    lives matter) OR blm OR racist OR racism OR (white supremacy) OR (white supremacist)"

    date_since = "2020-10-10"
    numTweets = 2500
    numRuns = 200

    extract_tweets(search_words, date_since, numTweets, numRuns)
