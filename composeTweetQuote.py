#!/usr/bin/python

import random
import os
import re
import sys
import subprocess
from TwitterAPI import TwitterAPI
import alart
import datetime
import math
import client
import tweet_codes
import argparse
import urllib

__author__ = "no3z"

MAX_QUOTE_LEN=201

### Define some functions for all different input possibilities

def createAlartPicture(image_name="/home/no3z/nfs/alart.png", alart_size = (1024,768)):
	class PoorRandomness(object):
	    def __init__(self):
	        self.state = 0.0

	    def random(self):
        	self.state = math.fmod(
	        self.state + datetime.datetime.now().microsecond / 1e6, 1)
	        return self.state

	    def randint(self, a, b):
        	return int(math.floor(self.random() * (b - a + 1))) + a

	#Create alart Image
	randomness = PoorRandomness()
	formats = ('png',)
	gen = alart.Alart(alart_size, formats, randomness)
	data = gen.generate()
	with open('%s' % image_name, 'wb') as f:
        	f.write(data['png'])

	return image_name

def getSplashImage(image_name="/home/no3z/nfs/splash.jpg"):
	splash = client.Client()
	json = splash.random
	res = urllib.urlopen(json['url'])
	output = open(image_name,"wb")
	output.write(res.read())
	output.close()
	return image_name

def getRandomImageFromDir(dir="/home/no3z/mission/images/"):
	files = [os.path.join(path, filename)
        	for path, dirs, files in os.walk(dir)
	        for filename in files
	        if not filename.endswith(".bak")]
	return random.choice(files)

def getSingleLineText(file):
	#Get Text
	lines = open(file).read().splitlines()
	quote=random.choice(lines)
	while not quote or len(quote) > MAX_QUOTE_LEN:
        	quote=random.choice(lines)
	quote=str(quote)
	quote=quote.replace("'","")
	return quote

def getMultiLineText(file):
	lines = open(file).read()
	myre = re.compile("(?s)(.*?)(?:(?:\r*\n){2})")
	things = myre.split(lines)
	quote=random.choice(things)
	while not quote or len(quote) > MAX_QUOTE_LEN:
        	print 'No valid quote'
	        quote=random.choice(things)
	quote=str(quote)
	quote=quote.replace("'","")
	return quote

def getFont(font_dir="/usr/share/fonts/truetype"):
	#Get Font
	files = [os.path.join(path, filename)
        	 for path, dirs, files in os.walk(font_dir)
	         for filename in files
	         if filename.endswith(".ttf")]
	font=random.choice(files)
	return font

# Let the argparse fun begin!

possible_image_source=["alart","splashbase","dir"]
parser = argparse.ArgumentParser(description="Tweet quotes with an image taken from multiple sources")
quote_group = parser.add_mutually_exclusive_group(required=True)
quote_group.add_argument('-sq','--quote_singleline', help='Single line quote text file')
quote_group.add_argument('-mq','--quote_multiline', help='Multi line quote text file')
parser.add_argument('-f','--font_dir', help="Font directory")
parser.add_argument('-o','--output_file', help="Output file", required=True)
parser.add_argument('-s','--image_source', help="Image source", required=True, choices=possible_image_source)
parser.add_argument('-d','--images_dir', help="Images directory for -dir- image source")
parser.add_argument('-t','--temp_img', help="Temp image location")

args = parser.parse_args()

if args.quote_singleline:
	quote = getSingleLineText(args.quote_singleline)
else:
	quote = getMultiLineText(args.quote_multiline)

if args.font_dir:
	 font = getFont(args.font_dir)
else:
	font = getFont()

if args.image_source == "alart":
	if not args.temp_img:
		image = createAlartPicture()
	else:
		 image = createAlartPicture(args.temp_img)
elif args.image_source == "splashbase":
	if not args.temp_img:
		image = getSplashImage()
	else:
		 image = getSplashImage(args.temp_img)
elif args.image_source == "dir":
	if not args.images_dir:
		print("You need to specify an image dir.")
		exit()
	image = getRandomImageFromDir(args.images_dir)

output_file = args.output_file

print quote
print image
print font

#Image magickk
text_ar = [(8.0,5.0),(4.0,3.0),(3.0,4.0),(5.0,8.0),(6.18,6.18)]
text_ar_factor = random.choice(text_ar)

width_cmd = ['identify', '-format', '%w', image]
width = subprocess.check_output(width_cmd)

height_cmd = ['identify', '-format', '%h', image]
height = subprocess.check_output(height_cmd)

print "Original size:" , width,"x",height
width = int(float(width) - (float(width)/text_ar_factor[0]))
height = int(float(height) - (float(height)/text_ar_factor[1]))

print "Text AR size:" , width,"x",height, text_ar_factor
size = str(width)+"x"+str(height)

background = "#ffffff00"
fill_styles = [("white","black"),("black","white")]
fill_styles_value = random.choice(fill_styles)
fill=fill_styles_value[0]
stroke=fill_styles_value[1]
strokewidth=random.choice(["3","2","4","1"])
gravity=random.choice(["center","north","south","west","east"])


# Now create image
cmd = "convert -size %s -background \'%s\' -font \'%s\' -fill %s -stroke %s -strokewidth %s caption:\'%s\' %s +swap -gravity %s -composite %s" % (size, background, font, fill, stroke, strokewidth, quote, image, gravity, output_file)
print cmd
convert = subprocess.Popen(cmd,shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE).communicate()

print "Convert output:",convert

#Tweet it
api = TwitterAPI(tweet_codes.consumer_key, tweet_codes.consumer_secret, tweet_codes.access_token, tweet_codes.access_token_secret)

# STEP 1 - upload image
file = open(output_file, 'rb')
data = file.read()
r = api.request('media/upload', None, {'media': data})
print('UPLOAD MEDIA SUCCESS' if r.status_code == 200 else 'UPLOAD MEDIA FAILURE')

# STEP 2 - post tweet with reference to uploaded image
if r.status_code == 200:
        media_id = r.json()['media_id']
        r = api.request('statuses/update', {'status':quote[0:140], 'media_ids':media_id})
        print('UPDATE STATUS SUCCESS' if r.status_code == 200 else 'UPDATE STATUS FAILURE')

file.close()

