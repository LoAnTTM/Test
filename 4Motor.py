import RPi.GPIO as GPIO
from shiftr_74HC595 import ShiftRegister
from time import sleep
import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Your pin definitions
DATA_PIN  = 10
CLOCK_PIN = 11
LATCH_PIN = 8

# For translating BCM → physical header and name
PIN_INFO = {
    DATA_PIN:  {"name": "DATA_PIN", "func": "SPI0_MOSI"},
    CLOCK_PIN: {"name": "CLOCK_PIN", "func": "SPI0_SCLK"},
    LATCH_PIN: {"name": "LATCH_PIN", "func": "SPI0_CE0_N"},
}

shift_register = ShiftRegister(DATA_PIN, LATCH_PIN, CLOCK_PIN)

def log_pin_details(pin):
    info = PIN_INFO[pin]
    func_code = GPIO.gpio_function(pin)
    if func_code == GPIO.IN:
        mode = "IN"
    elif func_code == GPIO.OUT:
        mode = "OUT"
    else:
        mode = "ALT"
    # only valid to read state if IN or OUT
    state = GPIO.input(pin) if mode in ("IN", "OUT") else None

    logger.info(
        f"{info['name']} → BCM {pin}, physical pin {info['phys']}, "
        f"alt‐func {info['func']}, mode {mode}, "
        f"state { 'HIGH' if state else 'LOW' if state is not None else 'N/A' }"
    )

def log_gpio_states():
    for pin in PIN_INFO:
        log_pin_details(pin)


def forward_all():
    outputs = [
        GPIO.HIGH, GPIO.LOW,   # Motor 1
        GPIO.HIGH, GPIO.LOW,   # Motor 2
        GPIO.HIGH, GPIO.LOW,   # Motor 3
        GPIO.HIGH, GPIO.LOW    # Motor 4
    ]
    shift_register.setOutputs(outputs)
    shift_register.latch()
    log_gpio_states()

def stop_all():
    outputs = [GPIO.LOW] * 8
    shift_register.setOutputs(outputs)
    shift_register.latch()

    log_gpio_states()

if __name__ == "__main__":
    try:
        logger.info("Motor control loop started. Commands: w=forward, s=stop, q=quit")
        while True:
            inp = input("> ").strip().lower()
            if inp == 'w':
                logger.info("→ Forward all motors for 5s")
                forward_all(5)
            elif inp == 's':
                logger.info("→ Stop all motors")
                stop_all()
            elif inp == 'q':
                logger.info("→ Quitting")
                break
            else:
                logger.warning("Invalid cmd '%s'. Use w, s or q.", inp)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
    finally:
        GPIO.cleanup()
        logger.info("GPIO cleaned up")
