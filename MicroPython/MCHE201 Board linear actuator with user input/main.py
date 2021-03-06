# -----------------------------------------------------------------------------
# main.py
#
# Script to demonstrate the taking user input on the desired length of the
# linear actuator, then using its potentiometer in a feedback controller 
# on its length. We use a simple on/off controller based on a deadzone around 
# the desired length. The pyboard is connected to the MCHE201 controller board.
#
# The linear actuator actually has a DC motor inside, so we control it 
# using the same commands that we would issue to a DC motor connected to the
# board.
#
# It also a potentiometer that can give us information about the position of 
# the actuator. Its value will be near Vcc (3.3VDC in this case) when fully 
# retracted and near 0VDC when fully extended. You should test your linear 
# actuator to determine the ADC values corresponding to its limits. They will
# vary slightly.
# 
# This script reads the value of the potentiometer, then using
# a mapping of its value to the actuator length to determine the current
# position of the actuator. This value is then used to generate the motor speed
# command for the actuator to drive the actuator to a desired length. If the
# actuator is outside a tolerable range around the desired length, it is moved
# at ~1/2 speed in the direction needed. Once within that tolerable range of 
# length it is stopped.
#
#
# The linear actuators in the MCHE 201 kits are:
#  https://www.servocity.com/hda4-2
#
# This code requires the .py files from the MCHE201 Controller Board repository
# found at:
#    https://github.com/DocVaughan/MCHE201_Controller
#
# Created: 03/26/19 - Joshua Vaughan - joshua.vaughan@louisiana.edu
#
# Modified:
#   * mm/dd/yy - Name (email if not same person as above)
#     - major change 1
#     - major change 2
#   * mm/dd/yy - Name (email if not same person as above)
#     - major change 1
#
# TODO:
#   * mm/dd/yy - Major bug to fix
#   # mm/dd/yy - Desired new feature
# -----------------------------------------------------------------------------

import pyb  # import the pyboard module
import time # import the time module (remove if not using)

# we need the copysign function from the math module 
# to determine what direction to move the actuator
from math import copysign 

# We'll use the machine i2c implementation.
import machine 

# We also need to import the linear actuator code from the library
import actuator

# Initialize communication with the motor driver
i2c = machine.I2C(scl=machine.Pin("X9"), sda=machine.Pin("X10"))

# And, then initialize the linear actuator control object
linear_actuator = actuator.LinearActuator(i2c)

# Set up the analog-to-digital converter to read the linear actuator 
# potentiometer that gives us information on its current length
linear_adc = pyb.ADC(pyb.Pin("X21"))

# We'll also define some constants for use in this code
# Change these two values to match those at the limits of your actuator.
ACT_MAX_ADC = 185  # ADC value at actuator maximum length
ACT_MIN_ADC = 4065 # ADC value at actuator minimum length

# These should be the same for all actuators in the MCHE201 kit
ACT_MAX_LEN = 3.93 # maximum stroke length (in)
ACT_MIN_LEN = 0.0  # minimum stroke length (in)

# This is the tolerance in our position control algorithm. If we are within
# this +/- of this distance of the desired length, we consider ourselves at 
# the desired position
LENGTH_TOLERANCE = 0.0625 # +/- 1/16in

# We'll now define a function that will convert a ADC value to actuator length
def calculate_length(adc_value):
    """ 
    This function uses a simple linear interpolation (y=mx+b) to estimate
    the current length of the linear actuator. It assumes a 4-inch stroke, like 
    those used in the MCHE201 kits
    
    Arguments:
      adc_value : the adc value (0-4095) to calculate the length for
      
    Returns:
      length : the calculated length
    """
    
    # calculate the slope and y-intercept for the linear fit
    slope = (ACT_MAX_LEN - ACT_MIN_LEN) / (ACT_MAX_ADC - ACT_MIN_ADC)
    intercept = ACT_MIN_LEN - slope * ACT_MIN_ADC
    
    # Now, calculate the length for the current ADC value
    length = slope * adc_value + intercept
    return length


# Now we'll run the main part of the script, which ask the user for an input, 
# processes it, checking its validity, then moves the actuator to the resulting
# desired length, using the actuator potentiometer for feedback on a simple
# on/off controller.
# 
# Note: This would be better done in a function if within a larger script.
try:
    while(True):
        # Read the potentiometer of the linear actuator, calculate initial length,
        # then print out its value
        linear_pot = linear_adc.read()
        linear_length = calculate_length(linear_pot)
        print("Current Length:    {:.2f}in".format(linear_length))

        # Now, we'll ask the user for their input
        print("Enter the desired stroke-length in inches, then press return:")
        desired_length_input = input()

        try:
            # convert to an integer desired length (in) <- Using inches to match actuator specs
            desired_length = float(desired_length_input) 
        except ValueError:
            print("Please enter a valid number.")
            print("Remaining at current length.")
            desired_length = linear_length
    
        # The simplest way to use the feedback is to just start moving toward the
        # desired length, then repeatedly check the length of the actuator. Once
        # it is within some tolerable bounds of the length, stop it. To do this, 
        # we...
    
        # Check that the desired length is within the bounds of the actuator
        if desired_length > ACT_MAX_LEN:
            desired_length = ACT_MAX_LEN - LENGTH_TOLERANCE
            print("The actuator is not that long.")
            print("Moving to maximum length of {:.2f}in instead.".format(desired_length))
        elif desired_length < ACT_MIN_LEN:
            desired_length = ACT_MIN_LEN + LENGTH_TOLERANCE
            print("The actuator cannot be that short.")
            print("Moving to minimum length of {:.2f}in instead.".format(desired_length))

        # Define the tolerable lengths around the desired values
        max_tolerable_length = desired_length + LENGTH_TOLERANCE
        min_tolerable_length = desired_length - LENGTH_TOLERANCE
    
        # Calculate the initial error
        length_error = desired_length - linear_length
    
        # Get the sign of the initial error. Used to set direction of motion.
        length_dir = copysign(1, length_error) 

        # Now, we can start the actuator at 1/2 speed toward the desired length
        linear_actuator.set_speed(int(length_dir)*50)
    
        # Then, keep moving while we are outside of the tolerable bounds around desired 
        while (linear_length > max_tolerable_length) or (linear_length < min_tolerable_length): 
            # Measure the length again
            linear_pot = linear_adc.read()
            linear_length = calculate_length(linear_pot)

            # Calculate the error
            length_error = desired_length - linear_length

            # Get the sign of the error for direction
            length_dir = copysign(1, length_error)
        
            # Print the current status
            print("Current Length:  {:>8.4f}in".format(linear_length))
            print("Length Error:    {:>8.4f}in\n".format(length_error))
        
            time.sleep_ms(1) # sleep 1ms

        # When the while loop breaks, we should be within our tolerable bounds
        # around the desired length. So, we stop the motor and report the final 
        # position
        linear_actuator.set_speed(0)
        print("\nStopped at {:.4f}in for a desired length of {:.2f}in.\n\n".format(linear_length, desired_length))

except:
    print("Error. Stopping motors.")
    linear_actuator.set_speed(0)
    
    # If we call raise here, we'll still get the information on why the 
    # exception was raised in the first place. Without this, we do not.
    raise 