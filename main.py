#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)
left_sensor = ColorSensor(Port.S1)
right_sensor = ColorSensor(Port.S4)

# Constants
BASE_SPEED = 210
TURN_SPEED = 25
GAIN = 1.45
LINE_COLOR = Color.BLACK
#LINE_COLOR = 25

# Line-following loop
while True:
    
    #left_color = left_sensor.color()
    #right_sensor.color() = right_sensor.color()

    if left_sensor.color() != LINE_COLOR and right_sensor.color() != LINE_COLOR:
        # Both sensors are off the line
        left_motor.run(speed=BASE_SPEED)
        right_motor.run(speed=BASE_SPEED)


    while left_sensor.color() == LINE_COLOR:
        right_motor.run(speed=TURN_SPEED)
        # Only the left sensor is on the line
        #left_motor.run(speed=BASE_SPEED)
        #right_motor.run(speed=BASE_SPEED * GAIN)
        #left_motor.run(speed=0)


    while right_sensor.color() == LINE_COLOR:
        left_motor.run(speed=TURN_SPEED)
        # Only the right sensor is on the line
        #left_motor.run(speed=BASE_SPEED * GAIN)
        #right_motor.run(speed=BASE_SPEED)
        #right_motor.run(speed=0)
    
    if left_sensor.color() == LINE_COLOR and right_sensor.color() == LINE_COLOR:
        # Both sensors are on the line
        left_motor.run(speed=-1)
        right_motor.run(speed=-1)

    

    # Update the EV3 brick display
    ev3.screen.clear()
    ev3.screen.print("Left: {}".format(left_sensor.color()))
    ev3.screen.print("Right: {}".format(right_sensor.color()))

    # Add a small delay to control the line-following speed
    wait(20)
