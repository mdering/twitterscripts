#!/usr/bin/env python

from twython import Twython
import time
import os.path
import json
import sqlite3
from tokens import *

#create a tweets.db sqlite file. 
#create a table like this:
#CREATE TABLE IF NOT EXISTS jsons (
#    id       INTEGER       PRIMARY KEY AUTOINCREMENT,
#    tweet_id VARCHAR (100) NOT NULL,
#    json     TEXT
#);


conn = sqlite3.connect('tweets.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS jsons (
    id       INTEGER       PRIMARY KEY AUTOINCREMENT,
    tweet_id VARCHAR (100) NOT NULL
                           UNIQUE ON CONFLICT REPLACE,
    json     TEXT
);''')

conn.commit();

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


f = open('matt_links.csv','r')

lastid="1";

query = "Select tweet_id from jsons order by id DESC LIMIT 1;"

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
	c.executemany('INSERT INTO jsons (tweet_id, json) VALUES (?,?)', inserts)
	conn.commit();
	print count, lineno*100
	print "sleeping for 5 seconds"
	time.sleep(5)
c.close()






