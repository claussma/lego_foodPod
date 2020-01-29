#!/usr/bin/env python3

"""
A small program to control a train based on LEGO Mindstorms EV3

Software on the Brick: https://www.ev3dev.org/

"""

import random
from time import sleep
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, LargeMotor, MediumMotor
from ev3dev2.sensor.lego import InfraredSensor, TouchSensor, ColorSensor

from ev3dev2.sound import Sound

__author__ = "Markus Clauß"
__copyright__ = "Copyright 2019, Markus Clauß"
__license__ = "GNU GPLv3"
__version__ = "1.0"


# connect to motors on ports B and C:
motors = [LargeMotor(add) for add in (OUTPUT_B, OUTPUT_C)]

# init infrared, touch and color sensors
#ir = InfraredSensor()
ts = TouchSensor()
cs = ColorSensor()

#  init small motor
sm = MediumMotor(OUTPUT_A)

# init sound
sound = Sound()



def start():
    """
    Start both motors. `run-direct` command will allow to vary motor
    performance on the fly by adjusting `duty_cycle_sp` attribute.
    """
    
    for m in motors:
        m.run_direct()

def motor_speed(speed):
    """
    set speed of the motors
    """
    global direction
    if direction:
        dc = speed
    else:
        dc = -speed

    for m in motors:
        m.duty_cycle_sp = dc

def run():
    """
    start moving
    """

    if state != -1:
        start()    
        motor_speed(speed)
    
def stop():
    """
    stop the robot
    """

    for m in motors:
        m.stop(stop_action='brake')

    #wait till stop
    while any(m.state for m in motors):
        sleep(0.1)

def turn():
    """
    turn the robot
    """
    global direction

    stop()
    direction = not direction
    color = cs.color

    run()
    while cs.color == color:
        sleep(0.2)
    

def mod_speed(pos, set=True, minspeed=10, maxspeed=100):
    """
    change the speed of the motors
    """
    global speed

    pos = abs(pos)

    if pos > 360:
        v = pos//360
        pos = pos - v*360

    pos = pos/360

    if pos < 0.1:
        pos = minspeed
    if pos > 100:
        pos = maxspeed

    speed = pos*maxspeed

    # BUG
    speed = 60

    if set:
        motor_speed(speed)

# init variables
direction = True

# state of the robot
# 0=start, 1=run, 2=wait, -1 = ERROR
state = 0

# how fast run the robot
speed = 0
mod_speed(sm.position, set=False)


# play a small song at start: Theme from Star Wars
sound.play_song((
     ('D4', 'e3'),      # intro anacrouse
     ('D4', 'e3'),
     ('D4', 'e3'),
     ('G4', 'h'),       # meas 1
     ('D5', 'h'),
     ('C5', 'e3'),      # meas 2
     ('B4', 'e3'),
     ('A4', 'e3'),
     ('G5', 'h'),
     ('D5', 'q'),
     ('C5', 'e3'),      # meas 3
     ('B4', 'e3'),
     ('A4', 'e3'),
     ('G5', 'h'),
     ('D5', 'q'),
     ('C5', 'e3'),      # meas 4
     ('B4', 'e3'),
     ('C5', 'e3'),
     ('A4', 'h.'),
     ))

#wait till push the button
while True:
    if ts.is_pressed:
        break

run()
while True:    
    #if ts.is_pressed:
    #    direction = not direction
    
    if cs.color in [ColorSensor.COLOR_RED, ColorSensor.COLOR_GREEN]:
        turn()
    
    #pos = abs(sm.position)
    #if pos != speed:
    #    mod_speed(pos)