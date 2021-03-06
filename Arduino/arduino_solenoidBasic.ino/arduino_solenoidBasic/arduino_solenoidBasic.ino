/*------------------------------------------------------------------------------------
arduino_solenoidBasic.ino

Retract a solenoid on a timer

For use with the Adafruit Motor Shield v2 
http://www.adafruit.com/products/1438

Adapted from the example code in the Adafruit library

Get the library at: 
https://github.com/ladyada/Adafruit_Motor_Shield_V2_Library/archive/master.zip

Created: 10/27/15 - Joshua Vaughan - joshua.vaughan@louisiana.edu

Modified:
  * 03/02/17 - Joshua Vaughan - joshua.vaughan@louisiana.edu
    - Changed max duty cycle of solenoid to better match its properties
  * mm/dd/yy - Name (email if not same person as above)
    - major change 1
    - major change 2
------------------------------------------------------------------------------------*/

// Include the necessary libraries for the motor shield
// You should include all three below anytime you're using the motor-driver shield
#include <Wire.h>
#include <Adafruit_MotorShield.h>
#include "utility/Adafruit_MS_PWMServoDriver.h"

// Create the motor shield object with the default I2C address
Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

// Select which 'port' M1, M2, M3 or M4. In this case, M4
Adafruit_DCMotor *solenoid = AFMS.getMotor(2);

void setup() {
  Serial.begin(9600);        // set up Serial library at 9600 bps

  AFMS.begin();  // create with the default frequency 1.6KHz

  // Set the speed to maximum for solenoid 
  // We want ~5V out... 5V out / 12V max ~= 100 duty cycle / 255 max duty cycle
  solenoid->setSpeed(100);
  
}


void loop() {    
    // full speed forward just passes maximum current to enable solenoid
    solenoid->run(FORWARD);
    
    // pause 10ms
    delay(100);
    
    // Stop the solenoid 
    solenoid->run(RELEASE); 
        
    // Delay for 1000 ms before continuing (avoiding solenoid burnout)
    delay(1000);
}
