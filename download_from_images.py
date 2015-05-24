#!/usr/bin/env python

from twython import Twython
import time
import os.path
import MySQLdb
import urllib
from tokens import *

conn = MySQLdb.connect(user=un,passwd=pw,db='mld284')
c = conn.cursor()

c.execute('select image_url from sd_images;')

row = c.fetchone()
rowno = 0

while row is not None:
	url=row[0]
	rowno+=1
	filename = url.split("/")[-1]
	if not os.path.exists("/data/Research/mld284/twitterimages/"+filename):
		#print url,filename
		time.sleep(.1)
		try:
			urllib.urlretrieve(url, "/data/Research/mld284/twitterimages/"+filename)
		except Exception as e:
			print e, url
			pass
	if rowno %100 == 0:
		print rowno
	row = c.fetchone()

