import spidev
import RPi.GPIO as GPIO
import time

# --- Cấu hình GPIO và PWM ---
GPIO.setmode(GPIO.BCM)
pwm_pins = {
    1: 18,  # EN1 → PWM0
    2: 19,  # EN2 → PWM1
    3: 13,  # EN3 → PWM1
    4: 12,  # EN4 → PWM0
}
pwms = {}
for motor, pin in pwm_pins.items():
    GPIO.setup(pin, GPIO.OUT)
    pwms[motor] = GPIO.PWM(pin, 1000)  # tần số 1 kHz
    pwms[motor].start(0)                # duty cycle ban đầu = 0%

# --- Cấu hình SPI (bus 0, device 0) ---
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000  # hoặc up to 1 MHz tùy shield

# --- Bảng mapping chiều quay ---
# Giả sử shift register xuất bit như sau:
#   bit 0/1 → Input1/Input2 của M1
#   bit 2/3 → Input1/Input2 của M2
#   bit 4/5 → Input1/Input2 của M3
#   bit 6/7 → Input1/Input2 của M4
dir_bits = {
    1: (0, 1),
    2: (2, 3),
    3: (4, 5),
    4: (6, 7),
}

def set_motor(motor, speed, forward=True):
    """
    motor: 1..4
    speed: 0..100
    forward: True = tiến, False = lùi
    """
    in1, in2 = dir_bits[motor]
    # tạo byte điều khiển chiều: chỉ 1 bit HIGH, bit còn lại LOW
    if forward:
        byte = (1 << in1)
    else:
        byte = (1 << in2)
    # gửi lên shift register và tự động latch via CS0
    spi.xfer([byte])
    # chỉnh tốc độ PWM
    pwms[motor].ChangeDutyCycle(speed)


def stop_motor(motor):
    """Dừng motor: duty cycle = 0 và clear hướng."""
    pwms[motor].ChangeDutyCycle(0)
    spi.xfer([0x00])


# --- Ví dụ chạy thử ---
try:
    # Chạy tiến 50% trong 2s
    for m in range(1, 5):
        set_motor(m, speed=50, forward=True)
    time.sleep(2)

    # Chạy lùi 50% trong 2s
    for m in range(1, 5):
        set_motor(m, speed=50, forward=False)
    time.sleep(2)

    # Dừng hết
    for m in range(1, 5):
        stop_motor(m)
    time.sleep(1)

except KeyboardInterrupt:
    pass

finally:
    # Giải phóng tài nguyên
    spi.close()
    for m in pwms.values():
        m.stop()
    GPIO.cleanup()
