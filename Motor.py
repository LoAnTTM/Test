import time
import machine as Pin

# Define the GPIO pins for the motor driver
in1 = Pin.Pin(24, Pin.OUT)
in2 = Pin.Pin(23, Pin.OUT)
in3 = Pin.Pin(22, Pin.OUT)
in4 = Pin.Pin(27, Pin.OUT)

# Motor control functions
def forward():
    in1.on()
    in2.off()
    in3.on()
    in4.off()

def backward():
    in1.off()
    in2.on()
    in3.off()
    in4.on()

def left():
    in1.on()
    in2.off()
    in3.off()
    in4.on()

def right():
    in1.off()
    in2.on()
    in3.on()
    in4.off()

def stop():
    in1.off()
    in2.off()
    in3.off()
    in4.off()

while True:
    forward()
    time.sleep(2)
    stop()
    time.sleep(1)

    backward()
    time.sleep(2)
    stop()
    time.sleep(1)

    left()
    time.sleep(2)
    stop()
    time.sleep(1)

    right()
    time.sleep(2)
    stop()
    time.sleep(1)
  