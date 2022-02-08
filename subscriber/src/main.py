from operator import imod
import time
import ubinascii
import machine

from machine import Pin, PWM
from umqttsimple import MQTTClient
from functions import closeValve
from config import MQTT_USER, MQTT_PASSWORD


pinLED = Pin(2, Pin.OUT)
pinLED.off()
pinServo = Pin(23, Pin.OUT)

pwmServo = PWM(pinServo)
pwmServo.freq(50)


MQTT_SERVER = 'maqiatto.com'

MQTT_PORT = 1883
SUB_TOPIC = 'vitorsorpile@gmail.com/gas_sensor'

def sub_cb(topic, msg):
    print( f'message {msg} arrived from topic {topic}')
    message = msg.decode('UTF-8')
    if topic == b'vitorsorpile@gmail.com/gas_sensor':
        try:
            value = float(message)
            print(value)
            if value <= 0.19:
                print('Gas leakage detected.')
                print('Closing valve...')
                closeValve(pwmServo)
        except:
            print('An exception occured.')



def connect_and_subscribe():
    client_id = ubinascii.hexlify(machine.unique_id())
    #   global client_id, mqtt_server, top ic_sub
    client_ = MQTTClient(client_id, MQTT_SERVER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client_.set_callback(sub_cb)
    client_.connect()
    client_.subscribe(SUB_TOPIC)
    print(f'Connected to {MQTT_SERVER} MQTT broker, subscribed to {SUB_TOPIC} topic')  
    return client_

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

pinLED.on()
while True:
    try:
        client.check_msg()
        
    except OSError as e:
        restart_and_reconnect()

