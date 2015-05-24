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

c.execute('''Create TABLE if not exists sd_images (
	id INT NOT NULL AUTO_INCREMENT,
	tweet_id VARCHAR (100) NOT NULL,
	image_url VARCHAR (300),
	PRIMARY KEY (id)
	);''')
conn.commit()

c.execute('select json from san_diego_jsons where json like "%media_url%";')

row = c.fetchone()
results=[]

while row is not None:
	js=row[0]
	data=json.loads(js)
	for pic in data['entities']['media']:
		#print data['id_str'],pic['media_url']
		results.append((data['id_str'],pic['media_url'])) 
	row = c.fetchone()
c.executemany("Insert into sd_images (tweet_id,image_url) Values (%s,%s)",results)
conn.commit()
conn.close()
exit()



