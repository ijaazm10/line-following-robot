#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

# Create your objects here.
ev3 = EV3Brick()

# Initialize the color sensors on ports 1 and 4
left_sensor = ColorSensor(Port.S4)
right_sensor = ColorSensor(Port.S1)
#left_touch_sensor = TouchSensor(Port.S2)
#right_touch_sensor = TouchSensor(Port.S3)
ultrasonic_sensor = UltrasonicSensor(Port.S3)  # Change the port to the one you are using

# Initialize the motors on ports B and C
left_motor = Motor(Port.D)
right_motor = Motor(Port.A)

# Create a DriveBase instance for controlling the motors
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=55, axle_track=135)

# Set the proportional steering constant
proportional_constant = 1.1

# Set the base speed and turn rate
base_speed = 80
turn_rate = 2.5

# Main loop
while True:

    #ev3.speaker.play_file(SoundFile.MOTOR_IDLE)
    # Flag to keep track of T-junction encounter
    #t_junction_encountered = False
    # Update the EV3 brick display
    ev3.screen.clear()
    ev3.screen.print("Deviation: {}".format(right_sensor.reflection() - left_sensor.reflection()))

    # Calculate the error for proportional steering
    error = (right_sensor.reflection() - left_sensor.reflection()) 
        
    # Calculate the turn rate based on the error
    if error in range(-25, 25):
        if left_sensor.reflection() < 15 and right_sensor.reflection() < 15: # and not t_junction_encountered:
            drive_base.drive(0, 0)    
            ev3.screen.print("Choose direction:")
            ev3.screen.print("1. Left")
            ev3.screen.print("2. Right")
            ev3.screen.print("3. Forward")
            ev3.screen.print("4. Backward")
            ev3.speaker.play_file(SoundFile.CONFIRM)
            while True:
                buttons = ev3.buttons.pressed()
                if Button.LEFT in buttons:
                    ev3.speaker.beep()
                    ev3.screen.clear()
                    ev3.screen.print("Turning Left")
                    drive_base.turn(70)
                    wait(500)
                    #t_junction_encountered = True
                    break
                elif Button.RIGHT in buttons:
                    ev3.speaker.beep()
                    ev3.screen.clear()
                    ev3.screen.print("Turning Right")
                    drive_base.turn(-70)
                    wait(500)
                    #t_junction_encountered = True
                    break
                elif Button.UP in buttons:
                    ev3.speaker.beep()
                    ev3.screen.clear()
                    ev3.screen.print("Moving Forward")
                    drive_base.drive(base_speed, 0)
                    wait(100)
                    #t_junction_encountered = True
                    break
                elif Button.DOWN in buttons:
                    ev3.speaker.beep()
                    ev3.screen.clear()
                    ev3.screen.print("Moving Backward")
                    drive_base.turn(-180)
                    wait(100)
                    #t_junction_encountered = True
                    break
        error = 0
    
     # Detect objects using ultrasonic sensor
    if ultrasonic_sensor.distance() < 100:  # Change the distance threshold as needed
        drive_base.drive(0, 0)  # Stop the robot if an object is detected
        ev3.speaker.play_file(SoundFile.DETECTED)
        drive_base.turn(-87)
        while right_sensor.reflection() > 15:
            drive_base.drive(base_speed, 22)
        wait(500)
        drive_base.drive(0, 0)
        drive_base.turn(-50)

    turn = turn_rate * error * proportional_constant

    # Drive the robot using the base speed and turn rate
    drive_base.drive(base_speed, turn)

    # Wait for a moment before the next iteration
    wait(10)