import Jetson.GPIO as GPIO
import time

# Physical board pin numbers
ENA = 32   # PWM0 (GPIO12)
IN1 = 11   # GPIO17
IN2 = 13   # GPIO27

# Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)

# Create PWM instance on ENA at 1kHz
pwm = GPIO.PWM(ENA, 1000)
pwm.start(0)  # Start with 0% duty

try:
    # Initial stop
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)
    time.sleep(1)

    # Forward at 70% speed
    print("Forward at 70% speed")
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
    print("Backward at 50% speed")
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
    print("✅ PWM stopped and GPIO cleaned up.")
