import RPi.GPIO as GPIO
from shiftr_74HC595 import ShiftRegister
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DATA_PIN  = 10   
CLOCK_PIN = 11   
LATCH_PIN = 8    

shift_register = ShiftRegister(DATA_PIN, LATCH_PIN, CLOCK_PIN)

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
    stop_all()

def stop_all():
    shift_register.setOutputs([GPIO.LOW]*8)
    shift_register.latch()

if __name__ == "__main__":
    try: 
        while True:
            inp = input()
            if inp == 'w':
                print("Run forward all motors for 5 seconds.")
                forward_all(5)
            elif inp == 's':
                print("Stop all motors.")
                stop_all()
            elif inp == 'q':
                print("Quit.")
                break
            else:
                print("Invalid command. Use w to move forward, q to quit.")
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
        print("GPIO cleaned up.")
