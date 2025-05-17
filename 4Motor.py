#!/usr/bin/env python3
import spidev
import RPi.GPIO as GPIO
import time

# --- Thiết lập GPIO/SPI ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Hủy mọi pin cũ (nếu có)
GPIO.cleanup()

# PWM pins cho M1–M4
pwm_pins = {1: 18, 2: 19, 3: 13, 4: 12}
pwms = {}
for m, pin in pwm_pins.items():
    GPIO.setup(pin, GPIO.OUT)
    pwms[m] = GPIO.PWM(pin, 1000)  # 1 kHz
    pwms[m].start(0)

# Mở bus SPI0, device CE0
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000

# Map bit shift register cho chiều
dir_bits = {
    1: (0, 1),
    2: (2, 3),
    3: (4, 5),
    4: (6, 7),
}

# --- Hàm điều khiển ---
def set_motor(m, speed, forward=True):
    # Chuyển đổi tốc độ từ 0-100% sang 0-255
    speed = int(speed * 2.55)
    if forward:
        GPIO.output(dir_bits[m][0], GPIO.HIGH)
        GPIO.output(dir_bits[m][1], GPIO.LOW)
    else:
        GPIO.output(dir_bits[m][0], GPIO.LOW)
        GPIO.output(dir_bits[m][1], GPIO.HIGH)
    pwms[m].ChangeDutyCycle(speed)
    print(f"Motor {m} {'forward' if forward else 'backward'} at {speed}%")
def stop_motor(m):
    pwms[m].ChangeDutyCycle(0)
    GPIO.output(dir_bits[m][0], GPIO.LOW)
    GPIO.output(dir_bits[m][1], GPIO.LOW)
    print(f"Motor {m} stopped")

def forward():
    for m in pwm_pins:
        set_motor(m, 50, forward=True)
    print("Moving forward...")
    time.sleep(2)

def backward():
    for m in pwm_pins:
        set_motor(m, 50, forward=False)
    print("Moving backward...")
    time.sleep(2)

def cleanup():
    for p in pwms.values():
        p.stop()
    GPIO.cleanup()
    print("GPIO cleaned up.")

# --- Thí dụ chạy thử ---
try:
    forward()
    time.sleep(1)
    backward()
    time.sleep(1)


except KeyboardInterrupt:
    print("Program interrupted by user.")

finally:
    spi.close()
    for p in pwms.values():
        p.stop()
    cleanup()
