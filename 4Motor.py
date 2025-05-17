#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

# --- Chân điều khiển 74HC595 ---
DATA_PIN  = 10  # MOSI (pin 19)
CLOCK_PIN = 11  # SCLK (pin 23)
LATCH_PIN = 8   # RCLK (pin 24)

# --- Chân PWM cho M1–M4 ---
PWM_PINS = {
    1: 18,  # EN1 → GPIO18
    2: 19,  # EN2 → GPIO19
    3: 13,  # EN3 → GPIO13
    4: 12,  # EN4 → GPIO12
}

# --- Setup GPIO ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

# 74HC595 pins
for pin in (DATA_PIN, CLOCK_PIN, LATCH_PIN):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# PWM pins
pwms = {}
for m, pin in PWM_PINS.items():
    GPIO.setup(pin, GPIO.OUT)
    pwms[m] = GPIO.PWM(pin, 1000)  # 1 kHz
    pwms[m].start(0)

# Map bit cho chiều quay
# bit 0/1 → M1, 2/3 → M2, 4/5 → M3, 6/7 → M4
DIR_BITS = {
    1: (0, 1),
    2: (2, 3),
    3: (4, 5),
    4: (6, 7),
}

def shift_byte(byte):
    """Đẩy 8 bit vào 74HC595 qua DATA/CLOCK, rồi latch."""
    GPIO.output(LATCH_PIN, GPIO.LOW)
    for i in range(7, -1, -1):
        GPIO.output(CLOCK_PIN, GPIO.LOW)
        GPIO.output(DATA_PIN, GPIO.HIGH if (byte & (1 << i)) else GPIO.LOW)
        GPIO.output(CLOCK_PIN, GPIO.HIGH)
    GPIO.output(LATCH_PIN, GPIO.HIGH)

def set_motor(motor, speed, forward=True):
    """
    speed: 0..100 (%)
    forward=True cho tiến, False cho lùi
    """
    in1, in2 = DIR_BITS[motor]
    # tạo byte: chỉ 1 bit HIGH
    byte = (1 << in1) if forward else (1 << in2)
    shift_byte(byte)
    pwms[motor].ChangeDutyCycle(speed)
    print(f"Motor {motor} {'forward' if forward else 'backward'} at {speed}%")

def stop_motor(motor):
    pwms[motor].ChangeDutyCycle(0)
    shift_byte(0x00)
    print(f"Motor {motor} stopped")

def forward(duration=2, speed=50):
    for m in PWM_PINS:
        set_motor(m, speed, forward=True)
    time.sleep(duration)
    print("Moving forward...")

def backward(duration=2, speed=50):
    for m in PWM_PINS:
        set_motor(m, speed, forward=False)
    time.sleep(duration)
    print("Moving backward...")

def cleanup():
    for p in pwms.values():
        p.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        while True:
            forward(2, 60)
            backward(2, 60)

    except KeyboardInterrupt:
        pass
    finally:
        cleanup()
