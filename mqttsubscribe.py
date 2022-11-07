import random

from paho.mqtt import client as mqtt_client


broker = '192.168.0.135'
port = 1883
global topic
topic = "IoTlab/termintensity"
global client_id
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'


global finalIntensity

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
 #   client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client



def subscribe():
    client = connect_mqtt()
    def on_message(client, userdata, msg):
#         global lightIntensity
        global lightIntensity 
#         lightIntensity = msg.payload.decode()
        lightIntensity = 4
        print (lightIntensity)
        return lightIntensity

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()

# finalIntensity = lightIntensity

if __name__ == '__main__':
    run()