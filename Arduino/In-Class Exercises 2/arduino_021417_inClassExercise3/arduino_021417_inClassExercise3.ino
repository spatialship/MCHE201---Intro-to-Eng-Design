/*------------------------------------------------------------------------------------
arduino_021417_inClassExercise3.ino

Connect the soft potentiometer and the piezo buzzer. Vary the pitch of the buzzer 
output based on where the soft potentiometer is pressed. Pressing at the “top” of 
the soft potentiometer should result in lower notes and the pressing at the “bottom” 
should result in higher pitches. See Circuit #10 from the SIK for help with the soft 
potentiometer and Circuit #11 from the SIK for help with the piezo buzzer.

http://arduino.cc/en/Tutorial/ReadAnalogVoltage

Created: 10/17/16 - Joshua Vaughan - joshua.vaughan@louisiana.edu

Modified:
  * 03/03/17 - JEV - joshua.vaughan@louisiana.edu
    - updated naming to match Spring 2017 assignment
    
------------------------------------------------------------------------------------*/

const int BUZZER_PIN = 9;

// This is always run once when the sketch starts
// Use to initialize variables, pin modes, libraries, communication, etc
void setup() {
  // set up the buzzer pin as an output
  pinMode(BUZZER_PIN, OUTPUT);
  
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
}

// the loop routine runs over and over again forever:
void loop() {
  
  // read the input on analog pin 0, which is where potentiometer is connected
  int sensor_value = analogRead(A0);

  // Uncomment below to output the sensor value for debugging
  // Serial.println(sensor_value);

  // Create a dead zone around 0, since the analog reading will not be exactly
  // zero when the sensor is not being touched. You may need to tune this to 
  // match your particular sensor.
  if (sensor_value > 50) {
    // Now, let's beep at a frequency proportional to the sensor reading
    tone(BUZZER_PIN, sensor_value+250);   // output a tone proportional to sensor_value
  }
  else { // not touching, so no sound
    noTone(BUZZER_PIN);
  }
  
  // Pause 10ms) between readings
  delay(10);
}
