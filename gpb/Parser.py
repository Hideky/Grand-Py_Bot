import requests
import ast
from . import views

stopwords = ast.literal_eval( open("gpb/fr.json", "r").read() )

# Split with stopword, requests google to get coordinate, return coordinate
class Parser:
	def __init__(self, data):
		self.config = views.app.config
		self.data = data

	# Re-define data (User's search) if necessary
	def set_data(self, data):
		self.data = data

	# Return data without stopword
	def get_essential(self): 
		return ' '.join([word for word in self.data.split() if word.lower() not in stopwords])

	# Get Coordinate from google map API using data
	def get_coordinate(self):
		url = 'https://maps.google.com/maps/api/geocode/json?address={}&key={}'
		print(self.get_essential())
		req = requests.get(url.format(self.get_essential() , self.config['GOOGLE_MAP_GEO_API_KEY']))
		if req.json()['status'] == 'ZERO_RESULTS':
			return None
		else:
			return req.json()['results'][0]['geometry']['location']
