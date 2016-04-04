#!/usr/bin/env python

from twython import Twython
import time
import os.path
import json
from tokens import *

#create a tweets.db sqlite file. 
#create a table like this:
#CREATE TABLE IF NOT EXISTS jsons (
#    id       INTEGER       PRIMARY KEY AUTOINCREMENT,
#    tweet_id VARCHAR (100) NOT NULL,
#    json     TEXT
#);


twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


f = open('boston100.txt','r')

g = open('bostonjsons.txt','w')
count = 0
lineno = 0
for line in f:
	l = line.strip()[:-1]
	lineno+=1
	tweets=twitter.lookup_status(id=l);
	inserts=[]
	for tweet in tweets:
		g.write(json.dumps(tweet)+"\n")
		count+=1
	print count, lineno*100
	print "sleeping for 5 seconds"






