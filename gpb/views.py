from flask import Flask, render_template, request
import logging
from logging import Formatter, FileHandler
import os
import requests
import wptools
import re
import ast

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


@app.route('/', methods=['POST'])
def result():
    search = request.form['search']
    stopwords_file  = open("gpb/fr.json", "r")
    stopwords = ast.literal_eval(stopwords_file.read())
    # Remove all stopwords and lower the first character remove him if it was a stopword
    if len(search.split(' ')) > 1:
        key = ' '.join([word for word in (search[:1].lower()+search[1:]).split(" ", 1)[1].split() if word not in stopwords])
    else:
        key = ' '.join([word for word in search.split(" ", 1)[0].split() if word not in stopwords])
    try:
        page = wptools.page(key.title(), lang='fr').get()
        if not page.data['exrest']:
            raise ValueError
    except:
         return render_template('pages/placeholder.notfound.html'), 404

    # If not real location but simple word OR list of many possible result
    if 'what' in page.data and page.data['what'] == "page d'homonymie de Wikimedia":
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', page.get().data['extract']).replace('&#160;', ' ')
        result_list = cleantext.split('\n')

        # Remove empty element from split
        result_list.pop(-1)

        if len(result_list) > 1:
            # Remove "**** can be refered at" and a empty element due to split
            del result_list[0]

            # Keeping essentials from result_list for next search (use in another result) 
            for i in range(0,len(result_list)):
                result_list[i] = result_list[i].split(',')[0].split('(')[0]
            # Retrieve data from first element of this list
            page = wptools.page(result_list.pop(0), lang='fr', silent=True).get()
            return render_template('pages/placeholder.result.html', message=page.data['exrest'], location=page.data['label'], another_result=result_list)
        
        # If word page but not list
        else:
            return render_template('pages/placeholder.result.html', message=page.data['exrest'], location=page.data['label'])
    else:
        return render_template('pages/placeholder.result.html', message=page.data['exrest'], location=page.data['label'])
        
@app.route('/another', methods=['POST'])
def another_result():
    another_result = ast.literal_eval(request.form['anotherResult'])
    page = wptools.page(another_result.pop(0), lang='fr', silent=True).get()

    # While not a page with unique subject
    while len(another_result) and (not page.get().data['extract'] or 'est un nom propre qui peut se référer à :' in page.get().data['exrest']):
        page = wptools.page(another_result.pop(0), lang='fr', silent=True).get()
    if page.get().data['extract']:
        return render_template('pages/placeholder.result.html', message=page.data['exrest'], location=page.data['label'], another_result=another_result)
    else:
        return render_template('pages/placeholder.notfound.html'), 404


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