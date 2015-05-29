#!/usr/bin/env python

from twython import Twython
import time
import os.path
import json
import MySQLdb
from tokens import *


f = open("tweets.txt")

images = []
urls = []
for line in f:
	tweet=line.strip().split("|")
	if len(tweet)>1:
		js = '|'.join(tweet[1:])
	else:
		continue
	data=json.loads(js)
	if 'entities' in data:
		if 'media' in data['entites']:
			for pic in data['entities']['media']:
				#print data['id_str'],pic['media_url']

				print data['id_str'],pic['media_url']
				urls.append(pic['media_url'])

rowno=0
for url in urls:
	rowno+=1
	filename = url.split("/")[-1]
	if not os.path.exists(filename):
		#print url,filename
		time.sleep(.1)
		try:
			urllib.urlretrieve(url, filename)
		except Exception as e:
			print e, url
			pass
	if rowno %100 == 0:
		print rowno
exit()



