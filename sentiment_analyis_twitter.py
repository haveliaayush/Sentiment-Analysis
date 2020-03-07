import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob

class TwitterData(object):
    def __init__(self):
        consumer_key = 'egw8IGWTCfaqxV0ZV4MWp42sw'
        consumer_secret = 'Epcheagt05RsWWJWX4Wwd4dZvxhGEf4UKn7a9d20HlW73Pd71n'
        access_token = '486545671-bZV2XaHHCSVxfEsWERVoun9W6LMrKquI0t19opU3'
        access_token_secret = 'm5cIHaaUP2VNNQGRPGBjf42f8QjbYtIo9cHKhHSEyZWXu'

        try:
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            self.auth.set_access_token(access_token, access_token_secret) 
            self.api = tweepy.API(self.auth) 
        except: 
            print("Error: Authentication Failed")
            
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())
    
    def get_tweet_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
            
    def get_tweets(self,query='ICICI',count=200):
        tweets = []
        try:
            fetched_tweets = self.api.search(q = query, count = count) 
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
                    
            return tweets
        
        except tweepy.TweepError as  e:
            print('Error : ',str(e))
            
def main():
    api = TwitterData()
    tweets = api.get_tweets(query = input('Enter bank name'), count = int(input('Enter number of queries to search')))
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    nutweets = [tweet for tweet in tweets if tweet['sentiment'] == 'neutral']
    print('Positive tweets percentage: {} %'.format(100*len(ptweets)/len(tweets)))
    print('Negative tweets percentage: {} %'.format(100*len(ntweets)/len(tweets)))
    print('Neutral tweets percentage: {} %'.format(100*(len(tweets) - len(ptweets) - len(ntweets))/len(tweets)))
              
if __name__ == "__main__" :
    main()