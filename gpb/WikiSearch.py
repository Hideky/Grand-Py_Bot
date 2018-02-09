import requests
import ast
from . import views

stopwords = ast.literal_eval( open("gpb/fr.json", "r").read() )

# Get subject from 
class WikiSearch:
	def __init__(self, location):
		self.location = location
		self.result = None

	# Re-define location if necessary
	def set_location(self, location):
		self.location = location

	# Return page's query using location
	def query(self): 
		url = 'https://fr.wikipedia.org/w/api.php?action=query&prop=coordinates&colimit=50&generator=geosearch&ggscoord={}|{}&ggsradius=1000&ggslimit=50&format=json'
		req = requests.get(url.format(self.location['lat'], self.location['lng']))
		if 'query' not in req.json():
			return None
		self.result = req.json()['query']['pages'].popitem()[1]
		return self.result

	# Extract 
	def extract(self):
		if not self.result:
			return None
		url = 'https://fr.wikipedia.org/w/api.php?action=query&prop=extracts&exchars=200&explaintext&pageids={}&format=json&exlimit=1'
		req = requests.get(url.format(self.result['pageid']))
		return req.json()['query']['pages'].popitem()[1]['extract']
