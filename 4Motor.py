import RPi.GPIO as GPIO
from shiftr_74HC595 import ShiftRegister
from time import sleep
import logging

# — Configure logging —
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

DATA_PIN  = 10
CLOCK_PIN = 11
LATCH_PIN = 8

shift_register = ShiftRegister(DATA_PIN, LATCH_PIN, CLOCK_PIN)

def log_gpio_states():
    # Read back Pi pins (they’re outputs, but you can still read their last state)
    data_state  = GPIO.input(DATA_PIN)
    clock_state = GPIO.input(CLOCK_PIN)
    latch_state = GPIO.input(LATCH_PIN)
    logger.info(f"GPIO pins → DATA({DATA_PIN}): {'HIGH' if data_state else 'LOW'}, "
                f"CLOCK({CLOCK_PIN}): {'HIGH' if clock_state else 'LOW'}, "
                f"LATCH({LATCH_PIN}): {'HIGH' if latch_state else 'LOW'}")

def log_sr_outputs(outputs):
    # outputs is a list of 8 HIGH/LOW values
    states = [ 'H' if o == GPIO.HIGH else 'L' for o in outputs ]
    # e.g. ['H','L','H',...]
    logger.info(f"Shift-register outputs Q0–Q7: {states}")

def forward_all(duration=2):
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
    sleep(duration)
    # stop_all()

def stop_all():
    outputs = [GPIO.LOW] * 8
    shift_register.setOutputs(outputs)
    shift_register.latch()
    log_sr_outputs(outputs)
    log_gpio_states()

if __name__ == "__main__":
    try:
        logger.info("Starting motor control loop. Commands: 'w' = forward, 's' = stop, 'q' = quit.")
        while True:
            inp = input("> ").strip().lower()
            if inp == 'w':
                logger.info("Command 'w' received: running all motors forward for 5s")
                forward_all(5)
            elif inp == 's':
                logger.info("Command 's' received: stopping all motors")
                stop_all()
            elif inp == 'q':
                logger.info("Command 'q' received: quitting")
                break
            else:
                logger.warning("Invalid command '%s'. Use w to move forward, s to stop, q to quit.", inp)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt, exiting.")
    finally:
        GPIO.cleanup()
        logger.info("GPIO cleaned up.")
