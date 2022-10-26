import firebase_admin  # pip install firebase_admin
from firebase_admin import db
import json

# Useful link for the future
# https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/

cred_obj = firebase_admin.credentials.Certificate('\piservice-firebase-adminsdk-6t0hc-e2400044da.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': 'https://piservice-default-rtdb.firebaseio.com/'})

ref = db.reference("/")

def create(json_data):
	db.set(json_data)

def read(querystring):

def update(key, column, value):

def delete(key):