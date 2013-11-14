#Creator: 		Maarten Zeinstra, Kennisland
#License: 		GNU GPL v3, for a full copy of the license go to http://opensource.org/licenses/GPL-3.0
#Description: 	This script takes a CSV as input to mass-upload already publicly available media files combined with a CSV with metadata to OpenBeelden.

import urllib, csv

apiKey = '' # Get you API key from your OpenBeelden Profile page
uploadURL = 'http://www.openbeelden.nl/api/media' #API URL
mediaURL = '' # Place your base URL here for you publicly accesible media files
location = '' # Place the local url of a CSV that contains your metadata

#First we will retrieve all media metadata from the CSV and put into a dict
metadata = csv.DictReader(open(location, 'rb'), delimiter=',', quotechar='"')

for mediaFile in metadata:
	#Do your mapping here
	data = {
		'apikey': apiKey,
		'url' 	: mediaURL + mediaFile['filename'], #combines the baseURL with the a filename, mind the extension
		'show' 	: False, # Show is set to false, to hide it from the public, use your profile page to publish the media file
		"license": "PDM", # Choose license here (cc-by-sa, cc-by, cc-by-nc, cc-by-nc-sa, cc-by-nd, cc-by-nc-nd, cc0, PDM)
		'title' : mediaFile['title'],
		'subtitle' : mediaFile['subtitle'],
		'language' : 'en', #en or nl
		'intro' : mediaFile['intro'],
		'body' : mediaFile['body'],
		'dc_creator' : mediaFile['director'] + ' / ' + mediaFile['producer'], # You can easily manipulate your metadata
		'keywords' : mediaFile['keywords'],
		'source' : mediaFile['source'] + mediaFile['catalogusID'],
		'coverage' : mediaFile['country'],
		'publisher' : mediaFile['producer'],
		'contributor' : mediaFile['Contributors'],
		'date' : mediaFile['creationDate'] # Only accepts datetime
	}
	
	# data will be converted into POST vars
	params = urllib.urlencode(data)
	
	#POST request will be send to API uploadURL
	data = urllib.urlopen(uploadURL, params).read()
	print data