import time
import Jetson.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

class Robot:
    def __init__(self):
        self.left_motor = [35, 36]
        self.right_motor = [37, 38]
        self.left_speed = 0
        self.right_speed = 0

        GPIO.setup(32, GPIO.OUT)  # ENA
        GPIO.setup(33, GPIO.OUT)  # ENB

        self.pwm = [GPIO.PWM(32, 50), GPIO.PWM(33, 50)]

        GPIO.setup(self.left_motor[0], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.left_motor[1], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.right_motor[0], GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.right_motor[1], GPIO.OUT, initial=GPIO.LOW)

        self.pwm[0].start(0)
        self.pwm[1].start(0)

    def _map_speed(self, value):
        return max(0, min(100, ((value + 1) / 2) * 100))  # converts -1~1 to 0~100%

    def set_motors(self, left_speed=1.0, right_speed=1.0):
        self.left_speed = self._map_speed(left_speed)
        self.right_speed = self._map_speed(right_speed)
        self.pwm[0].ChangeDutyCycle(self.left_speed)
        self.pwm[1].ChangeDutyCycle(self.right_speed)

    def forward(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.HIGH)
        GPIO.output(self.left_motor[1], GPIO.LOW)
        GPIO.output(self.right_motor[0], GPIO.HIGH)
        GPIO.output(self.right_motor[1], GPIO.LOW)
        self.set_motors(speed, speed)

    def backward(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.LOW)
        GPIO.output(self.left_motor[1], GPIO.HIGH)
        GPIO.output(self.right_motor[0], GPIO.LOW)
        GPIO.output(self.right_motor[1], GPIO.HIGH)
        self.set_motors(speed, speed)

    def left(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.LOW)
        GPIO.output(self.left_motor[1], GPIO.HIGH)
        GPIO.output(self.right_motor[0], GPIO.HIGH)
        GPIO.output(self.right_motor[1], GPIO.LOW)
        self.set_motors(speed, speed)

    def right(self, speed=1.0):
        GPIO.output(self.left_motor[0], GPIO.HIGH)
        GPIO.output(self.left_motor[1], GPIO.LOW)
        GPIO.output(self.right_motor[0], GPIO.LOW)
        GPIO.output(self.right_motor[1], GPIO.HIGH)
        self.set_motors(speed, speed)

    def stop(self):
        for pin in self.left_motor + self.right_motor:
            GPIO.output(pin, GPIO.LOW)
        self.pwm[0].ChangeDutyCycle(0)
        self.pwm[1].ChangeDutyCycle(0)

    def cleanup(self):
        self.stop()
        self.pwm[0].stop()
        self.pwm[1].stop()
        GPIO.cleanup()


if __name__ == "__main__":
    robot = Robot()
    try:
        print("=== Control your robot using W A S D keys (Q to quit) ===")
        while True:
            command = input("Enter command (w/a/s/d to move, q to quit): ").strip().lower()
            if command == 'w':
                robot.forward()
            elif command == 's':
                robot.backward()
            elif command == 'a':
                robot.left()
            elif command == 'd':
                robot.right()
            elif command == 'q':
                break
            else:
                print("Invalid command. Use w/a/s/d to move, q to quit.")
            time.sleep(0.1)
    finally:
        robot.stop()
        robot.cleanup()
        print("GPIO cleaned up. Motors stopped.")
