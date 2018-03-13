###############################################################################
# main.py
#
# This script is one way to solve the 7th in-class exercise from MCHE201 in the
# spring semester of 2018.
#
# # That exercise was given as:
#  * Attach a potentiometer
#  * Have the servo angle track the angle of the potentiometer
#
# Script to run a servo motor connected to the pyb.Servo(1) pin on the board, 
# based on a potentiometer reading. The servo should track the potentiometer.
# See note in script for what physical pin this corresponds to on the version
# of the pyboard that you have.
#
#
# Created: 03/08/18
#   - Joshua Vaughan
#   - joshua.vaughan@louisiana.edu
#   - http://www.ucs.louisiana.edu/~jev9637
#
# Modified:
#   * 
#
# TODO:
#   * 
###############################################################################

import pyb  # import the pyboard module
import time # import the time module

# Define the servo object. The numbering scheme differs between the pyboard and
# the pyboard LITE.
# 
# For the pyboard:
#  Servo 1 is connected to X1, Servo 2 to X2, Servo 3 to X3, and Servo 2 to X4
#
# For the pyboard LITE:
#  Servo 1 is connected to X3, Servo 2 to X4, Servo 3 to X1, and Servo 2 to X2

# Here, we'll use the first position on the pyboard
servo1 = pyb.Servo(1)

# Define constants for the min and max servo angles allowed
MAX_SERVO_ANGLE = 75
MIN_SERVO_ANGLE = -75

# Set up the analog-to-digital converter (ADC) for the potentiometer
pot_adc = pyb.ADC(pyb.Pin("X22"))


def potADCtoServoAngle(ADC_value):
    """ This function converts a potentiometer reading of 0-4095 to an angle
    between MIN_SERVO_ANGLE and MAX_SERVO_ANGLE, using the global 
    representation for those angle extremes
    
    The middle of the potentiometer range, 2048, should map to 0deg servo angle
    The max. of the range, 4095, should map to MAX_SERVO_ANGLE
    The min. of the range, 0, should map to MIN_SERVO_ANGLE
    
    Inputs: 
      ADC_value : a number between 0 and 4095 representing a reading 
                  from the poteniometer
    
    Returns:
      angle : The angle to move the servo to to match the potentiomter angle
    """
    
    # define the slope and intercept for the line mapping ADC_value to angle
    slope = (MAX_SERVO_ANGLE - MIN_SERVO_ANGLE) / 4095
    intercept = -slope * 2048
    
    # Now, calculate the angle output based on that linear function
    angle = slope * ADC_value + intercept
    
    return angle
    
    

# Now read the pot and move the servo every 10ms, forever
while (True):

    # Read the value of the potentiometer. It should be in the range 0-4095
    pot_value = pot_adc.read()
    
    desired_angle = potADCtoServoAngle(pot_value)

    # print out the values, nicely formatted
    print("The ADC value is {:d}, moving servo to {:.2f} deg".format(pot_value, desired_angle))

    servo1.angle(desired_angle)
    
    time.sleep_ms(10)
