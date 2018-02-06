import os
import unittest
import requests
import json
from ..WikiSearch import WikiSearch

# Created a Mock class with json function to match with 'requests' operation
class MockResponse:
    def __init__(self, file):
        path = os.path.join('gpb', 'tests', 'data', file)
        self.data = open(path, encoding='utf-8').read()
    def json(self):
        return json.loads(self.data)

class TestWikiSearch:
    instance = WikiSearch({"lat": 47.218371, "lng": -1.553621})

    def test_instance(self):
        assert isinstance(self.instance, WikiSearch)

    # Testing query from wikimedia API using coordinate
    def test_query(self, monkeypatch):
        def mockreturn(requests):
            return MockResponse('mock_query_wikimedia.json')

        monkeypatch.setattr(requests, 'get', mockreturn)
        assert self.instance.query() == mockreturn("").json()['query']['pages'].popitem()[1]
    
    # Testing extract from wikimedia API using pageid previously retrieved by "test_query"
    def test_extract(self, monkeypatch):
        def mockreturn(requests):
            return MockResponse('mock_extract_wikimedia.json')

        monkeypatch.setattr(requests, 'get', mockreturn)
        assert self.instance.extract() == mockreturn("").json()['query']['pages'].popitem()[1]['extract']
    