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

f = open("bostonjsons.txt",'r')
g  = open("bostonimages.txt",'w')

for row in f:
	js=row.strip()
	data=json.loads(js)
	if 'media' in data['entities']:
		for pic in data['entities']['media']:
			#print data['id_str'],pic['media_url']
			g.write(pic['media_url']+"\n") 
g.close()



