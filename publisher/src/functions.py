from time import sleep
from machine import PWM

def playBuzzer(pwmBuzzer: PWM):
    pwmBuzzer.freq(512)
    pwmBuzzer.init()

    for _ in range(3):
        pwmBuzzer.duty(512)
        sleep(1)
        pwmBuzzer.duty(0)
        sleep(0.5)

    # pwmBuzzer.duty(50)B
    pwmBuzzer.deinit()
