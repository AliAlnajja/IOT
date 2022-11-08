import random
import time

from paho.mqtt import client as mqtt_client #https://pypi.org/project/paho-mqtt/#installation

# setting up all that is needed for the client connection to mwtt broker
broker = "192.168.1.52" # server (IP from photoresistor_complete.ino)
port = 1883 #does not change
topic = "IoTlab/termintensity" # topic published by photoresistor_complete.ino
client_id = f'python-mqtt-{random.randint(0, 100)}' # initializing client as arandom

def subscribe(): #whole method to subscribe to the server
    def on_message(client, userdata, msg): # making a message, I dont know why we have userdata, but that is the way it is everywhere and nowhere is it explained
        #global lightIntensity #-- was to return at the end of subscribe()
        lightIntensity = msg.payload.decode() # setting value recieved from server to lightIntensity value
        if lightIntensity == '' or lightIntensity == None: #discarding null values
            pass
        else:
            print(lightIntensity) # printing out needed value
#             return lightIntensity
#         print("lightIntensity=", lightIntensity)
    client = mqtt_client.Client(client_id) #initializing the client
    client.on_message = on_message
    client.connect(broker, port) #connecting to the server
    client.loop_start() # start loop
    client.subscribe(topic) #subscribing to the topic
    client.publish(topic)
    time.sleep(4) # sleep so only one value is printed out
    client.loop_stop() # stop loop
    # return lightIntensity # was to send to app.py
def run():
    subscribe()


if __name__ == '__main__':
    run()