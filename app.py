from flask import Flask, render_template, redirect, url_for, request
from PIL import Image
from PIL.ExifTags import TAGS
import random
import reverse_geocoder as rg 
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/image/<image_url>')
def predicton(image_url):
	# path to the image or video
	imagename = "static/" + image_url + ".jpg"
	print(imagename)
	# read the image data using PIL
	image = Image.open(imagename)
	exifdata = image.getexif()
	tags = {}
	# Put tags into dict
	for tag_id in exifdata:
		tag = TAGS.get(tag_id, tag_id)
		data = exifdata.get(tag_id)
		if isinstance(data, bytes):
			data = data.decode()
		tags[tag] = data
		print(tag)
		print(data)
	# extract gps coordinates
	# if statements account for W or S gps values (which should be negative)
	lat = float(tags['GPSInfo'].get(2)[0]) + float(tags['GPSInfo'].get(2)[1])/60 
	if tags['GPSInfo'].get(1)[0] == 'S':
		lat = lat * -1
	lng = float(tags['GPSInfo'].get(4)[0]) + float(tags['GPSInfo'].get(4)[1])/60 
	if tags['GPSInfo'].get(3)[0] == 'W':
		lng = lng * -1
	locationDict = rg.search((lat,lng))[0]
	location = locationDict.get('name') + ', ' + locationDict.get('admin1') 
	
	
	return render_template('image.html', tags=tags, image_url = "../" + imagename, location=location)

if __name__ == '__main__':
	app.run()