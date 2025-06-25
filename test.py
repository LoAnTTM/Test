import RPi.GPIO as GPIO
import time

# Setup pin numbers
ENA = 32   # Enable pin with PWM (Pin 32 = GPIO12)
IN1 = 11   # Direction
IN2 = 13

# Use physical pin numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Set up pins
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Create PWM instance on ENA pin at 1kHz
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)  # Start with 0% duty cycle (stopped)

try:
    # Stop initially
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
    time.sleep(1)

    # Forward at 70% speed
    print("Running forward at 70% speed")
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(70)
    time.sleep(2)

    # Stop
    print("Stop")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
    time.sleep(1)

    # Backward at 50% speed
    print("Running backward at 50% speed")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(50)
    time.sleep(2)

    # Final stop
    print("Final stop")
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
    time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")
