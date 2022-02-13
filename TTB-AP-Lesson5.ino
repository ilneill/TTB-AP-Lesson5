// Using an Arduino with Python LESSON 5: Analog Voltage Meter in vPython.
// https://www.youtube.com/watch?v=noqZ8QFzJxc
// https://toptechboy.com/using-an-arduino-with-python-lesson-5-analog-voltage-meter-in-vpython/

// Defines.
#define POTPIN A0

// Global variables.
int readDelay=100;
int potValue;

void setup() {
    // Initialise the potentiometer pin.
    pinMode(POTPIN,INPUT);
    // Start the serial port.
    Serial.begin(115200);
}

void loop() {
    // Read the potentiometer value.
    potValue=analogRead(POTPIN);
    // Send the potentiometer value to the serial port.
    Serial.println(potValue);
    // Wait for a bit...
    delay(readDelay);
}

//EOF
