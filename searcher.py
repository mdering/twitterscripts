#!/usr/bin/env python

from twython import Twython
from twython import TwythonStreamer
import time

import io
from urllib2 import urlopen

from tokens import *

f=open("superbowltweets.csv",'w')

api = Twython(APP_KEY, APP_SECRET,
					OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
tweets						  =   []
MAX_ATTEMPTS					=   10
COUNT_OF_TWEETS_TO_BE_FETCHED   =   500 

for i in range(0,MAX_ATTEMPTS):
	if(COUNT_OF_TWEETS_TO_BE_FETCHED < len(tweets)):
		print "done"
		break # we got 500 tweets... !!

	#----------------------------------------------------------------#
	# STEP 1: Query Twitter
	# STEP 2: Save the returned tweets
	# STEP 3: Get the next max_id
	#----------------------------------------------------------------#

	# STEP 1: Query Twitter
	if(0 == i):
		# Query twitter for data. 
		results	= api.search(q='#SuperBowl', since='2015-02-02', until='2015-02-02',count='100')
	else:
		# After the first call we should have max_id from result of previous call. Pass it in query.
		results	= api.search(q='#SuperBowl', since='2015-02-02', until='2015-02-02',include_entities='true',max_id=next_max_id)

	# STEP 2: Save the returned tweets
	for result in results['statuses']:
		tweet_text = result['text']
		tweets.append(tweet_text)
		print tweet_text

	# STEP 3: Get the next max_id
	try:
		# Parse the data returned to get max_id to be passed in consequent call.
		print "more pages"
		next_results_url_params	= results['search_metadata']['next_results']
		next_max_id		= next_results_url_params.split('max_id=')[1].split('&')[0]
	except:
		print "no more pages"
		# No more next pages
		break
	time.sleep(2500)
for tweet in tweets:
	f.write(tweet+"\n")
f.close()
