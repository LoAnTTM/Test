import time
import RPi.GPIO as GPIO

# Khai báo chân theo số BCM
IN1 = 24
IN2 = 23
IN3 = 22
IN4 = 27

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in (IN1, IN2, IN3, IN4):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def left():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def right():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def stop():
    for pin in (IN1, IN2, IN3, IN4):
        GPIO.output(pin, GPIO.LOW)

def cleanup():
    stop()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        while True:
            forward()
            time.sleep(2)


    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
        print("GPIO cleaned up.")
