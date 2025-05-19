import RPi.GPIO as GPIO
from shiftr_74HC595 import ShiftRegister
import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin definitions
DATA_PIN  = 10
CLOCK_PIN = 11
LATCH_PIN = 8

# Map BCM → physical header and function
PIN_INFO = {
    DATA_PIN:  {"name": "DATA_PIN",  "phys": 19, "func": "SPI0_MOSI"},
    CLOCK_PIN: {"name": "CLOCK_PIN", "phys": 23, "func": "SPI0_SCLK"},
    LATCH_PIN: {"name": "LATCH_PIN", "phys": 24, "func": "SPI0_CE0_N"},
}

shift_register = ShiftRegister(DATA_PIN, LATCH_PIN, CLOCK_PIN)

def log_pin_details(pin):
    info = PIN_INFO[pin]
    func_code = GPIO.gpio_function(pin)
    mode = "IN" if func_code == GPIO.IN else "OUT" if func_code == GPIO.OUT else "ALT"
    state = GPIO.input(pin) if mode in ("IN", "OUT") else None
    logger.info(
        f"{info['name']} → BCM {pin}, physical pin {info['phys']}, "
        f"alt‐function {info['func']}, mode {mode}, "
        f"state { 'HIGH' if state else 'LOW' if state is not None else 'N/A' }"
    )

def log_gpio_states():
    for pin in PIN_INFO:
        log_pin_details(pin)

def log_sr_outputs(outputs):
    states = ['H' if o == GPIO.HIGH else 'L' for o in outputs]
    logger.info(f"Shift‐register Q0–Q7 outputs: {states}")

def forward_all():
    outputs = [
        GPIO.HIGH, GPIO.LOW,   # Motor 1
        GPIO.HIGH, GPIO.LOW,   # Motor 2
        GPIO.HIGH, GPIO.LOW,   # Motor 3
        GPIO.HIGH, GPIO.LOW    # Motor 4
    ]
    shift_register.setOutputs(outputs)
    shift_register.latch()
    log_sr_outputs(outputs)
    log_gpio_states()

def stop_all():
    outputs = [GPIO.LOW] * 8
    shift_register.setOutputs(outputs)
    shift_register.latch()
    log_sr_outputs(outputs)
    log_gpio_states()

if __name__ == "__main__":
    try:
        logger.info("Motor control loop started. Commands: w = forward, s = stop, q = quit")
        while True:
            cmd = input("> ").strip().lower()
            if cmd == 'w':
                logger.info("Command 'w' received: starting all motors until 's' is entered")
                forward_all()
            elif cmd == 's':
                logger.info("Command 's' received: stopping all motors")
                stop_all()
            elif cmd == 'q':
                logger.info("Command 'q' received: exiting program")
                break
            else:
                logger.warning("Invalid command '%s'. Use w, s, or q.", cmd)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
    finally:
        GPIO.cleanup()
        logger.info("GPIO cleaned up")
