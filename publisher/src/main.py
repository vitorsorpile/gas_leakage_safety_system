import time
import ubinascii
import machine
import micropython
from machine import PWM, Pin, ADC
from umqttsimple import MQTTClient
from functions import playBuzzer
from MQ2 import getRatio, calculateR0
from pins import *
from config import MQTT_USER, MQTT_PASSWORD


MQTT_SERVER = 'maqiatto.com'
MQTT_PORT = 1883

SUB_TOPIC = 'vitorsorpile@gmail.com/gas_sensor'

leakageDetected = False

def connect():
    client_id = ubinascii.hexlify(machine.unique_id())
    #   global client_id, mqtt_server, top ic_sub
    client_ = MQTTClient(client_id, MQTT_SERVER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    # client.set_callback(sub_cb)
    client_.connect()
    # client.subscribe(SUB_TOPIC)
    # print('Connected to %s MQTT broker, subscribed to %s topic' % (MQTT_SERVER, SUB_TOPIC))
    return client_

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect()
except OSError as e:
    restart_and_reconnect()

print('Warming up sensor...')
for _ in range(10):
    pinLEDconnected.value(not pinLEDconnected.value())
    time.sleep(1)

print('Finished warming up.')
pinLEDconnected.on()

# calculateR0()


while True:
    # tmpFile = open('clearAirMeasures.txt', 'w')
    count = 0
    try:
        # value = MQGetGasPercentage(MQRead(pins.adcGasSensor)/Ro,GAS_LPG)
        # value = 0
        # for _ in range(50):
        #     value += adcGasSensor.read()
        #     time.sleep(0.1)
        # value = value/50
        # print(value*10000)
        value = getRatio()
        print(value)
        client.publish(SUB_TOPIC, str(value), qos=1)

        count += 1

        if value < 0.19:
            leakageDetected = True
            break
        
        if count == 100:
            break
        time.sleep(1)

        # time.sleep(5)
        # client.check_msg()
        # if (time.time() - last_message) > message_interval:
        #   msg = b'Hello #%d' % counter
        #   client.publish(SUB_TOPIC, b'received')
        #   last_message = time.time()
        #   counter += 1
    except OSError as e:
        restart_and_reconnect()

if leakageDetected:
    pinLEDleakage.on()
    while True:
        playBuzzer(pwmBuzzer)
