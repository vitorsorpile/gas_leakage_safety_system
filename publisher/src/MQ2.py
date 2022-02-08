from time import sleep
import math
import pins

def calculateR0():
    sensorValue = 0
    for _ in range(100):
        sensorValue += pins.adcGasSensor.read()
        sleep(0.1)

    sensorValue /= 100

    sensorValue = sensorValue * 5.0 / 3.33

    sensorVolt = sensorValue/4096*5.0
    RS_air = (5.0 - sensorVolt)/sensorVolt
    R0 = RS_air/9.83
    print(f'R0 is {R0}')

    return R0

def getRatio():
    sensor_volt = 0
    RS_gas = 0 # Get value of RS in a GAS
    # ratio = 0 # Get ratio RS_GAS/RS_air
    sensorValue = pins.adcGasSensor.read()

    sensorValue = sensorValue * 5.0 / 3.33

    sensor_volt= sensorValue/4096*5.0
    RS_gas = (5.0-sensor_volt)/sensor_volt # omit *RL
    R0 = 0.3
    #/*-Replace the name "R0" with the value of R0 in the demo of First Test -*/
    ratio = RS_gas/R0 # ratio = RS/R0
    # print(ratio)
    return ratio
    #/*-----------------------------------------------------------------------*/
    # Serial.print("sensor_volt = ");
    # Serial.println(sensor_volt);
    # Serial.print("RS_ratio = ");
    # Serial.println(RS_gas);
    # Serial.print("Rs/R0 = ");
    # Serial.println(ratio);
    # Serial.print("\n\n");
    # delay(1000);
