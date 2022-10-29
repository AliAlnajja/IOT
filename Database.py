import firebase_admin  # pip install firebase_admin
from firebase_admin import db
import json

# Useful link for the future
# https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/

# Database connection
cred_obj = firebase_admin.credentials.Certificate('\piservice-firebase-adminsdk-6t0hc-e2400044da.json')
default_app = firebase_admin.initialize_app(cred_obj, {'databaseURL': 'https://piservice-default-rtdb.firebaseio.com/'})

# Sector of Realtime DB
ref = db.reference("/")

# Method to create data in the database (will be improved)
def createUser():
	db.set(json_data)

def read(querystring):

def update(key, column, value):
	users = ref.get()
	for k, v, in users.items():
		if (v["user_id"] == key):
			ref.child(k).update({column = value})

def delete(key):