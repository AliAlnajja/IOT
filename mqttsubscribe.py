import random
import time

from paho.mqtt import client as mqtt_client


broker = "192.168.1.52"
port = 1883
topic = "IoTlab/termintensity"
client_id = f'python-mqtt-{random.randint(0, 100)}'

def subscribe():
    def on_message(client, userdata, msg):
        lightIntensity = msg.payload.decode()
        if lightIntensity == '' or lightIntensity == None:
            pass
        else:
            print(lightIntensity)
#             return lightIntensity
#         print("lightIntensity=", lightIntensity)
    client = mqtt_client.Client(client_id)
    client.on_message = on_message
    client.connect(broker, port)
    client.loop_start()
    client.subscribe(topic)
    client.publish(topic)
    time.sleep(4)
    client.loop_stop()
def run():
    subscribe()


if __name__ == '__main__':
    run()