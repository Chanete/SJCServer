import sys
import paho.mqtt.client

def on_connect(client, userdata, flags, rc):
    global nombre
    print('Conexion a MQTT server establecida (%s)' % client._client_id)
    client.subscribe(topic='broadlink/#', qos=2)
    client.publish("broadlink/recordrf",nombre)
 
 

def on_message(client, userdata, message):
    print('-------- RECEIVED ------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print('qos: %d' % message.qos)    

def on_publish(client, userdata, message):
    print('------- PUB -----------------------')
    print('topic: %s' % message.topic)
    print('payload: %s' % message.payload)
    print('qos: %d' % message.qos)    



if (len(sys.argv) < 2):
    print("Falta nombre grabacion")
    sys.exit(12)

nombre=sys.argv[1]
print("GRabando %s" % nombre)


client = paho.mqtt.client.Client(client_id='GrabaIR-Mqtt', clean_session=True)
client.on_connect = on_connect
client.on_message = on_message
#client.on_publish = on_publish
client.connect_async(host='192.168.1.199', port=1883)

#client.publish("STAT/SwBot/Finger_Long/","OFF")
print("Switchbot MQTT Connected to MQTT Server. Starting loop")
client.loop_forever()