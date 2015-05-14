#!/usr/bin/env python

from twython import Twython
import time
import os.path
import json
import MySQLdb
from tokens import *

#create a tweets.db sqlite file. 
#create a table like this:
#CREATE TABLE IF NOT EXISTS jsons (
#    id       INTEGER       PRIMARY KEY AUTOINCREMENT,
#    tweet_id VARCHAR (100) NOT NULL,
#    json     TEXT
#);


conn = MySQLdb.connect(user=un,passwd=pw,db='mld284')
c = conn.cursor()

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


f = open('fixed_sdlinks.csv','r')

lastid="1";

query = "Select tweet_id from san_diego_jsons order by id DESC LIMIT 1;"

c.execute(query);

fetch = c.fetchone()
if fetch is None:
	lastid="1";
	cont=0
else:
	#print fetch
	lastid=str(fetch[0])
	cont =1

count = 0
lineno = 0
for line in f:
	l = line.strip()
	lineno+=1
	if lastid in l:
		cont=0
	if cont==1:
		continue;
	tweets=twitter.lookup_status(id=l);
	inserts=[]
	for tweet in tweets:
		inserts.append((tweet['id_str'],json.dumps(tweet)))
		count+=1
	c.executemany('INSERT INTO san_diego_jsons (tweet_id, json) VALUES (%s,%s)', inserts)
	conn.commit();
	print count, lineno*100
	print "sleeping for 5 seconds"
	time.sleep(5)
c.close()






