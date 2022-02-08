from time import sleep

def closeValve(pwmServo):
    pwmServo.init()
    sleep(2)
    # 20 -> 0 graus
    # 70 -> 90 graus
    # 120 -> 180 graus
    pwmServo.duty(70)
    sleep(2)
    pwmServo.deinit()
