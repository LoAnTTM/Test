#!/usr/bin/env python3
import spidev
import RPi.GPIO as GPIO
import time

# --- Thiết lập GPIO và SPI ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Hủy mọi cài trước đó (nếu có)
GPIO.cleanup()

# PWM pins cho M1–M4
pwm_pins = {
    1: 18,  # EN1 → GPIO18 (PWM0)
    2: 19,  # EN2 → GPIO19 (PWM1)
    3: 13,  # EN3 → GPIO13 (PWM1)
    4: 12,  # EN4 → GPIO12 (PWM0)
}
pwms = {}
for m, pin in pwm_pins.items():
    GPIO.setup(pin, GPIO.OUT)
    pwms[m] = GPIO.PWM(pin, 1000)  # tần số 1 kHz
    pwms[m].start(0)                # duty cycle ban đầu bằng 0%

# Mở bus SPI0, device CE0 (pin 24 = GPIO8 làm latch)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000

# Map bit shift-register cho chiều quay:
# bit 0/1 → Inputs M1, 2/3 → M2, 4/5 → M3, 6/7 → M4
dir_bits = {
    1: (0, 1),
    2: (2, 3),
    3: (4, 5),
    4: (6, 7),
}

def set_motor(motor, speed, forward=True):
    """
    Bật motor #motor (1..4):
      speed: 0..100 (%) → duty cycle
      forward=True cho tiến, False cho lùi
    """
    in1, in2 = dir_bits[motor]
    # tạo byte: chỉ một trong hai bit HIGH
    byte = (1 << in1) if forward else (1 << in2)
    # gửi qua SPI (tự động latch bằng CE0)
    spi.xfer([byte])
    # điều chỉnh tốc độ
    pwms[motor].ChangeDutyCycle(speed)
    print(f"Motor {motor} {'forward' if forward else 'backward'} at {speed}%")

def stop_motor(motor):
    """Dừng motor #motor, tắt PWM và reset hướng."""
    pwms[motor].ChangeDutyCycle(0)
    spi.xfer([0x00])
    print(f"Motor {motor} stopped")

def forward(duration=2, speed=50):
    """Chạy tiến tất cả motor trong duration giây."""
    for m in pwm_pins:
        set_motor(m, speed, forward=True)
    print("Moving forward...")
    time.sleep(duration)

def backward(duration=2, speed=50):
    """Chạy lùi tất cả motor trong duration giây."""
    for m in pwm_pins:
        set_motor(m, speed, forward=False)
    print("Moving backward...")
    time.sleep(duration)

def cleanup():
    """Dọn dẹp SPI và GPIO trước khi thoát."""
    spi.close()
    for p in pwms.values():
        p.stop()
    GPIO.cleanup()
    print("Cleaned up GPIO and SPI.")

if __name__ == "__main__":
    try:
        forward(duration=2, speed=60)
        backward(duration=2, speed=60)
        # dừng sau cùng
        for m in pwm_pins:
            stop_motor(m)
    except KeyboardInterrupt:
        print("Interrupted by user.")
    finally:
        cleanup()
