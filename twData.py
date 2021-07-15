
# First step is to define our keys so we can gett access to Twitter API

import tweepy as tw
import pandas
import re
import sys
from textblob import TextBlob
from collections import defaultdict
ptweets = []
ntweets = []
neutral = []
neutralCounter = 0
ptcounter = 0
ntcounter = 0

# Define the search term and the date_since date as variables
date_since = "2020-03-01"

def twitter_auth():
    """
    Handles authentication handshaking with the Twitter API
    """

    access_token = "1352473741117145088-9ga2flQ1nSqtWufLQr8GM1BHZwAyOT"

    access_token_secret = "JF3aQai1DEsjWayDuI4ebDiffIDWcLrzqtBKRvZX3Qu5Q"


    consumer_key = "QkReevsCWcMXrlcAtB9YQSf5W"
    consumer_secret = "cf79J99kqFzB3CKsp9dLZq37rHSSuUZB9kaj7FLAWOXGLVif27"


    auth =  tw.OAuthHandler(consumer_key, consumer_secret)

    auth.set_access_token(access_token, access_token_secret)

    api = tw.API(auth, wait_on_rate_limit=True)
    
    return api



def clean_tweet(tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

def get_sentiment(tweet):

    tweet = clean_tweet(tweet.text)
    analysis = TextBlob(tweet)
    global ntcounter
    global ptcounter
    global neutralCounter
    global neutral
    global ptweets
    global ntweets
  

    if analysis.sentiment.polarity > 0:
        ptcounter += 1
        ptweets.append(tweet)
        return
    
    elif analysis.sentiment.polarity < 0:
        ntcounter += 1
        ntweets.append(tweet)
        return
    
    else:
        if analysis.sentiment.polarity == 0:
            neutralCounter += 1
            neutral.append(tweet)
            return


def main(argv):
    search_words = sys.argv[-1]
    #search_words = "@UCDavisMedCntr"
    api = twitter_auth()
    geo='34.0722,-118.4441,500mi'        # lat,long for UCLA 

    # Collect tweets
    tweets_raw = [ tweet for tweet in tw.Cursor(api.search, q=search_words, geocode=geo, lang="en", since=date_since).items(200) if tweet.user.location ]
    

    for tweet in tweets_raw:
        #print(tweet.user.location)
        get_sentiment(tweet)
    
    # print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets_raw))) 
    # print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets_raw))) 
    # print("Neutral tweets percentage: {} %".format(100*len(neutral)/len(tweets_raw))) 

    data = ""
    data += str(ntcounter) + " "    
    data += str(neutralCounter) + " "
    data += str(ptcounter)

    print(data)
    return


 


if __name__ == '__main__':
    main(sys.argv[-1])
    
