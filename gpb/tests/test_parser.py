import os
import unittest
import requests
import json
from ..Parser import Parser

# Created a Mock class with json function to match with 'requests' operation
class MockResponse:
    def __init__(self, file):
        path = os.path.join('gpb', 'tests', 'data', file)
        self.data = open(path, encoding='utf-8').read()
    def json(self):
        return json.loads(self.data)

class TestParser:

    instance = Parser('')

    def test_instance(self):
        assert isinstance(self.instance, Parser)

    # Testing Simple parsing
    def test_parsing_essential_1(self):
        parser = self.instance.set_data("Raconte moi une histoire sur Nantes")
        assert self.instance.get_essential() == "Nantes"
    
    # Testing Simple parsing
    def test_parsing_essential_2(self):
        parser = self.instance.set_data("A tu quelque chose sur Antarès au Mans ?")
        assert self.instance.get_essential() == "Antarès Mans"
    
    # Testing Simple parsing
    def test_parsing_essential_3(self):
        parser = self.instance.set_data("Raconte moi quelque chose sur Grand-Py Bot")
        assert self.instance.get_essential() == ""
    
    # Testing parsing to get location
    def test_parsing_location_1(self, monkeypatch):    
        def mockreturn(requests):
            return MockResponse('mock_coordinate.json')
    
        monkeypatch.setattr(requests, 'get', mockreturn)
        assert self.instance.get_coordinate() == {"lat": 47.218371, "lng": -1.553621} # Or MockResponse.json()['results'][0]['geometry']['location']