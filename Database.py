import pyrebase #pip3 install Pyrebase4
import shutil
import os

config = {
	"apiKey": "AIzaSyAygkmVV4K-kmyLKnTW4oy9DCUcuAQZ_aw",
	"authDomain": "piservice.firebaseapp.com",
	"databaseURL": "https://piservice-default-rtdb.firebaseio.com/",
	"projectId": "piservice",
	"storageBucket": "piservice.appspot.com",
	"messagingSenderId": "91557331901",
	"appId": "1:91557331901:web:f458ffc2cca448cb8a08d4",
	"measurementId": "G-VQW24SCDYV",
	"serviceAccount": "serviceAccountKey.json"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

def formatUserJson(name, max_temp, max_humid, max_light):
	data = {
		"Name" : name,
		"Temp_Threshold" : max_temp,
		"Humid_Threshold" : max_humid,
		"Light_Threshold" : max_light,
		"Profile_Image" : "anonymousProfile.png"
	}
	return data


def userIsNull(rfid_key):
	return db.child(rfid_key).get().val() == None


def createUser(rfid_key, name, max_temp, max_humid, max_light):	
	if userIsNull(rfid_key):
		db.child(rfid_key).set(formatUserJson(name, max_temp, max_humid, max_light))
	else:
		updateUser(rfid_key, formatUserJson(name, max_temp, max_humid, max_light))


def getUserInfo(rfid_key):
	if userIsNull(rfid_key) is False:
		return db.child(rfid_key).get().val()
	else:
		print("Invalid user. Please enter a valid user RFID key.")


def updateUser(rfid_key, user_data):
	if userIsNull(rfid_key) is False:
		db.child(rfid_key).update(user_data)
	else:
		print("Invalid user. Please enter a valid user RFID key.")


def updateUserInfo(rfid_key, column, value):
	if userIsNull(rfid_key) is False:
		db.child(rfid_key).update({column : value})
	else:
		print("Invalid user. Please enter a valid user RFID key.")


def deleteUser(rfid_key):
	if userIsNull(rfid_key) is False:
		db.child(rfid_key).remove()
	else:
		print("Invalid user. No user was deleted.")


def parseUserData(userData):
	print(userData["Name"])
	print(userData["Temp_Threshold"])
	print(userData["Humid_Threshold"])
	print(userData["Light_Threshold"])
	print(userData["Profile_Image"])


def uploadProfileImage(rfid_key, fileExtension):
	storage.child(rfid_key).put("./assets/userImages/" + rfid_key + fileExtension)
	updateUserInfo(rfid_key, "Profile_Image", rfid_key)
	shutil.rmtree("./assets/userImages")
	os.mkdir("./assets/userImages")


def downloadProfileImage(rfid_key):
	shutil.rmtree("./assets/userImages")
	os.mkdir("./assets/userImages")
	if getUserInfo(rfid_key)["Profile_Image"] == "anonymousProfile.png":
		storage.child("anonymousProfile.png").download("anonymousProfile.png", "profile.png")
	else:
		storage.child(rfid_key).download(rfid_key, "profile.png")
	shutil.move("./profile.png", "./assets/userImages/profile.png")
