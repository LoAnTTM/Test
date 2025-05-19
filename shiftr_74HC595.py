import logging
import RPi.GPIO as GPIO

# Configure logging at the module level
logging.basicConfig(
    format="%(asctime)s %(levelname)s: %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

class ShiftRegister:
    register_type = '74HC595'

    """
    data_pin  => pin 14 on the 74HC595
    latch_pin => pin 12 on the 74HC595
    clock_pin => pin 11 on the 74HC595
    """
    def __init__(self, data_pin, latch_pin, clock_pin):
        self.data_pin  = data_pin
        self.latch_pin = latch_pin
        self.clock_pin = clock_pin

        # Set up pins
        GPIO.setup(self.data_pin,  GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        self.outputs = [GPIO.LOW] * 8

        # Log initial pin configuration
        logger.info(
            f"ShiftRegister init: DATA={self.data_pin}, "
            f"CLOCK={self.clock_pin}, LATCH={self.latch_pin}"
        )
        logger.debug(f"Initial outputs: {self.outputs}")

    def setOutput(self, output_number, value):
        if not 0 <= output_number < 8:
            raise ValueError("Invalid output number. Must be 0–7.")
        self.outputs[output_number] = value
        logger.debug(f"setOutput: Q{output_number} -> {'HIGH' if value else 'LOW'}")

    def setOutputs(self, outputs):
        if len(outputs) != 8:
            raise ValueError("setOutputs must be a list of 8 elements.")
        self.outputs = outputs
        pretty = ['H' if v == GPIO.HIGH else 'L' for v in outputs]
        logger.debug(f"setOutputs: Q0–Q7 -> {pretty}")

    def latch(self):
        # Prepare to shift bits
        logger.debug("Starting latch sequence")
        GPIO.output(self.latch_pin, GPIO.LOW)
        logger.debug(f"LATCH pin {self.latch_pin} -> LOW")

        # Shift out each bit, MSB first
        for i in range(7, -1, -1):
            bit = self.outputs[i]
            GPIO.output(self.clock_pin, GPIO.LOW)
            GPIO.output(self.data_pin,  bit)
            logger.debug(
                f"Clock LOW, Data -> Q{i} = {'HIGH' if bit else 'LOW'}"
            )

            GPIO.output(self.clock_pin, GPIO.HIGH)
            logger.debug(f"Clock HIGH (pulsed)")

        # Latch the shifted data
        GPIO.output(self.latch_pin, GPIO.HIGH)
        logger.debug(f"LATCH pin {self.latch_pin} -> HIGH")
        logger.info("Latch complete, outputs updated on shift register")
