import random
import time

from paho.mqtt import client as mqtt_client


broker = "192.168.2.141"
port = 1883
global topic
topic = "/IoTlab/lightIntensity"
topic2 = "/IoTlab/rfidVals"
global client_id
client_id = f'python-mqtt-{random.randint(0, 100)}'

lightIntensity = 0
rfidVal = ""

def subscribe():
    def on_message(client, userdata, msg):
        global lightIntensity
        global rfidVal
        if msg.topic == topic:
            lightIntensity = float(msg.payload.decode())
            if(lightIntensity != '' and lightIntensity != None):
                print(lightIntensity)
        
        if msg.topic == topic2:
            rfidVal = msg.payload.decode().strip().replace(" ", ":")
            print(rfidVal)
    client = mqtt_client.Client(client_id)
    client.on_message = on_message
    client.connect(broker, port)
    
    client.subscribe(topic)
    client.subscribe(topic2)
    client.loop_start()

def run():
    subscribe()


if __name__ == '__main__':
    run()

run()