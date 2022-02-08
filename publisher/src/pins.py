from machine import Pin, PWM, ADC

pinLEDconnected = Pin(0, Pin.OUT)
pinLEDconnected.off()

pinLEDleakage = Pin(2, Pin.OUT)
pinLEDleakage.off()

pinBuzzer = Pin(23, Pin.OUT)
pwmBuzzer = PWM(pinBuzzer)

pwmBuzzer.deinit()

pinGasSensor = Pin(32)
adcGasSensor = ADC(pinGasSensor, atten= ADC.ATTN_11DB)
