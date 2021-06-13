import csv
import twitter
from twitter import TwitterError

import twitter_credentials

corpusFile = "corpus.csv"
tweetDataFile = "tweetDataFile.csv"

# initialize api instance
twitter_api = twitter.Api(consumer_key=twitter_credentials.CONSUMER_KEY,
                          consumer_secret=twitter_credentials.CONSUMER_SECRET,
                          access_token_key=twitter_credentials.ACCCESS_TOKEN,
                          access_token_secret=twitter_credentials.ACCESS_TOKEN_SECRET)

corpus = []
with open(corpusFile, 'rt') as csvfile:
    lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
    for row in lineReader:
        corpus.append({"tweet_id": row[2], "label": row[1], "topic": row[0]})

trainingDataSet = []

for tweet in corpus:
    try:
        status = twitter_api.GetStatus(tweet["tweet_id"])
        print("Tweet fetched: " + status.text)
        tweet["text"] = status.text
        trainingDataSet.append(tweet)
    except TwitterError as err:
        print("Error while fetching tweet ID " + tweet["tweet_id"] + ". Message: " + err.message[0]["message"])

# Now we write them to the empty CSV file
with open(tweetDataFile, 'wt') as csvfile:
    linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
    for tweet in trainingDataSet:
        try:
            linewriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
        except Exception as e:
            print(e)
