import os
import unittest
from .. import views

class ViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = views.app
        self.app.config.from_object('config')
        self.app.testing = True
        self.app = views.app.test_client()

    # def tearDown(self):

    # Testing Home Page
    def test_home(self):
    	assert self.app.get('/').status_code == 200

    # Testing About Page
    def test_about(self):
    	assert self.app.get('/about').status_code == 200

    # Testing Result Page
    def test_result(self):
    	assert self.app.get('/search', query_string={'search':"Racontre moi une histoire sur Paris"}).status_code == 200

    # Testing Result Page with random input
    def test_false_result(self):
        assert self.app.get('/search', query_string={'search':"ùpdskfgmskdgmkds"}).status_code == 404