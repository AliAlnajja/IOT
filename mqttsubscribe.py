import random
import time

from paho.mqtt import client as mqtt_client #https://pypi.org/project/paho-mqtt/#installation

# setting up all that is needed for the client connection to mwtt broker
broker = "192.168.1.52" # server (IP from photoresistor_complete.ino)
port = 1883
topic = "IoTlab/termintensity" # topic published by photoresistor_complete.ino
client_id = f'python-mqtt-{random.randint(0, 100)}'

def subscribe(): #whole method to subscribe to the server and return lightIntensity
    def on_message(client, userdata, msg): 
        global lightIntensity # to be able to return at the end of subscribe()
        lightIntensity = msg.payload.decode() # setting value recieved from server to lightIntensity value
        intIntensity = lightIntensity[:-3]
        lightIntensity = intIntensity
        if lightIntensity == '' or lightIntensity == None: #discarding null values
            pass
        else:
            print(lightIntensity)
    client = mqtt_client.Client(client_id) #initializing the client
    client.on_message = on_message
    client.connect(broker, port) #connecting to the server
    client.loop_start()
    client.subscribe(topic)
    client.publish(topic)
    time.sleep(4) # sleep so only one value is printed out
    client.loop_stop()
    return lightIntensity # to send to app.py


if __name__ == '__main__':
    subscribe()
