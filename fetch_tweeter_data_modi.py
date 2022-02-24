""" Script to fetch all tweets so far from Narendra Modi (India's PM) tweeter's account and save them in CSV"""

import tweepy
import csv
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#Twitter API credentials, please put your own credentials here
consumer_key = "*************"
consumer_secret = "*************"
access_key = "*************"
access_secret = "*************"

def clean_tweet(tweet):
    '''
    Function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z' \t])|(\w+:\/\/\S+)", " ", tweet).split())




def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,exclude_replies=True,lang="en",tweet_mode='extended')
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,exclude_replies=True,lang="en",max_id=oldest,tweet_mode='extended')
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, clean_tweet(tweet.full_text).replace('\n', '').replace('\r', '').replace('|','')] for tweet in alltweets if (not tweet.retweeted) and ('RT @' not in tweet.full_text) ]
	
    result=[]
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
 		writer = csv.writer(f, delimiter='|')
		writer.writerow(["id","timestamp","words"])
                for items in outtweets:
                  out=items[2]
                  index = items[0]
                  time=items[1]
                  x=out.split()
                  for w in x:
        	      writer.writerow((index ,time, w))
		
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("narendramodi")