import os

basedir = os.path.abspath(os.path.dirname(__file__))
GOOGLE_API_KEY = 'AIzaSyBTao_6kKLddi60VyJAO-RitjJJ1v-gc8s'
SECRET_KEY = '\rC\n\t$%Dmy;EXQn~5pJM_0Y28'
# Connect to the database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')