import pandas as pd
from tqdm import tqdm
import demoji

TWEETS_FILEPATH = "<path to the extracted tweets csv file>"
OUTFILE = "<path for output file>"

def get_emoji(text):
    """
    For each detected emoticon, this function return the corresponding name viz. "hundred points", "smiling face with
    halo", "US flag" etc.
    :param text: tweet text
    :return: set of detected emoticons in a tweet
    """
    emoticons = demoji.findall(text)
    return set(emoticons.values())


def remove_emoji(text):
    """
    This function removes all special characters that may or may not represent an emoticon and convert to lower case.
    :param text: tweet text
    :return: cleaned text
    """
    return ''.join([ch for ch in text if ch.isalnum() or ch == " "]).lower()


if __name__ == "__main__":
    df_tweets = pd.read_csv(TWEETS_FILEPATH, encoding="utf-8")
    print("Looking for emoticons...")
    tqdm.pandas()
    df_tweets["emoticons"] = df_tweets["text"].progress_apply(get_emoji)
    print("Cleaning the text...")
    df_tweets["text"] = df_tweets["text"].progress_apply(remove_emoji)
    df_tweets.to_csv(OUTFILE, index=False)
