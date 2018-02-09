from flask import Flask, render_template, request, Response
import logging
from logging import Formatter, FileHandler
import os
import requests
import re
import ast
import json
from .Parser import Parser
from .WikiSearch import WikiSearch

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')

# Controller

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/search', methods=['GET'])
def result():
    parser = Parser(request.args.get('search'))
    wikisearch = WikiSearch(parser.get_coordinate())
    
    if not wikisearch.query():
        return Response(status=404, mimetype='application/json')

    data = {
        'description':  wikisearch.extract(),
        'location': wikisearch.location
    }
    js = json.dumps(data)

    return Response(js, status=200, mimetype='application/json')
        


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# if __name__ == "__main__":
#     app.run()