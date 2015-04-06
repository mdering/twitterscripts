#!/usr/bin/env python

from twython import Twython
from twython import TwythonStreamer

import io
from PIL import Image, ImageTk

import Tkinter as tk
from urllib2 import urlopen

from tokens import *


class MyStreamer(TwythonStreamer):
	fence=[[-77.798924,40.749326],[-77.917295,40.817749]]
	def on_success(self, data):
		name=data['user']['screen_name']
		if not self.test_coordinates(data):
			return
		#print data['coordinates'], data['place']
		print 'passed'
		if 'text' in data:
			print name.encode('utf-8')+": "+data['text'].encode('utf-8')
		if 'media' in data['entities']:
			#print len(data['entities']['media'])
			for i in range(0,len(data['entities']['media'])):
				pic = data['entities']['media'][i]
				self.show_pic(pic,i,name)
		

	def on_error(self, status_code, data):
		print status_code

		# Want to stop trying to get data because of the error?
		# Uncomment the next line!
		# self.disconnect()
	def show_pic(self, pic,i,name):
		root =tk.Tk()
		root.title(name+"'s photo "+str(i+1))
		image_url = pic['media_url']
		image_bytes = urlopen(image_url).read()
		data_stream = io.BytesIO(image_bytes)
		pil_image = Image.open(data_stream)
		w, h = pil_image.size
		tk_image = ImageTk.PhotoImage(pil_image)
		label = tk.Label(root, image=tk_image, bg='brown')
		label.pack(padx=5, pady=5)
		root.mainloop()
	def test_coordinates(self,data):
		name=data['user']['screen_name']
		#print name.encode('utf-8')+": "+data['text'].encode('utf-8')
		#print data['coordinates'], data['place']
		return True
		if data['coordinates'] is None:
			return False
		longitude= data['coordinates']['coordinates'][0]
		latitude=data['coordinates']['coordinates'][1]
		print latitude,longitude
		if longitude<self.fence[0][0] or longitude >self.fence[1][0]:
			return False
		if latitude<self.fence[0][1] or latitude >self.fence[1][1]:
			return False
		return True


stream = MyStreamer(APP_KEY, APP_SECRET,
					OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='#SuperBowl since:2015-02-01 until:2015-02-02')


