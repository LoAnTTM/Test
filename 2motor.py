import Jetson.GPIO as GPIO
import time
import sys
import termios
import tty

# GPIO pin setup
IN1 = 11  
IN2 = 13  
ENA = 15  

IN3 = 16  
IN4 = 18  
ENB = 22  

GPIO.setmode(GPIO.BOARD)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

pwmA = GPIO.PWM(ENA, 1000)
pwmB = GPIO.PWM(ENB, 1000)

pwmA.start(0)
pwmB.start(0)

def get_key():
    """Read a single key press (without Enter)"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

def stop():
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    print("⏹️ Stop")

def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(70)
    pwmB.ChangeDutyCycle(70)
    print("⬆️ Forward")

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(70)
    pwmB.ChangeDutyCycle(70)
    print("⬇️ Backward")

def turn_left():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(20)
    pwmB.ChangeDutyCycle(70)
    print("⬅️ Turn Left")

def turn_right():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(70)
    pwmB.ChangeDutyCycle(20)
    print("➡️ Turn Right")

try:
    print("=== Control your motors using W A S D keys (Q to quit) ===")
    while True:
        key = get_key().lower()

        if key == 'w':
            forward()
        elif key == 's':
            backward()
        elif key == 'a':
            turn_left()
        elif key == 'd':
            turn_right()
        elif key == 'q':
            stop()
            break
        else:
            stop()

finally:
    pwmA.stop()
    pwmB.stop()
    GPIO.cleanup()
    print("✅ GPIO cleaned up. Exiting.")
