import RPi.GPIO as GPIO
from shiftr_74HC595 import ShiftRegister
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DATA_PIN  = 10   
CLOCK_PIN = 11   
LATCH_PIN = 8    

shift_register = ShiftRegister(DATA_PIN, CLOCK_PIN, LATCH_PIN)

def forward_all(duration=2):
    outputs = [
        GPIO.HIGH, GPIO.LOW,   # Motor 1
        GPIO.HIGH, GPIO.LOW,   # Motor 2
        GPIO.HIGH, GPIO.LOW,   # Motor 3
        GPIO.HIGH, GPIO.LOW    # Motor 4
    ]
    shift_register.setOutputs(outputs)
    shift_register.latch()
    sleep(duration)

def stop_all():
    shift_register.setOutputs([GPIO.LOW]*8)
    shift_register.latch()

if __name__ == "__main__":
    try:
        print("Run forward all motors for 3 seconds.")
        forward_all(3)
        print("Stop all motor.")
        stop_all()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
