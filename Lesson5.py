# !/usr/bin/env python3

# Using an Arduino with Python LESSON 5: Analog Voltage Meter in vPython.
# https://www.youtube.com/watch?v=noqZ8QFzJxc
# https://toptechboy.com/using-an-arduino-with-python-lesson-5-analog-voltage-meter-in-vpython/

# Internet References:
# https://www.glowscript.org/docs/VPythonDocs/index.html

import time
import serial
from vpython import *
import numpy as np

# Visual Python refresh rate.
vPythonRate = 250

# All dimensions are relative to allow easier meter scaling.
meterScale = 1.0

# Draw the meter box.
meterBoxX = 2.5 * meterScale
meterBoxY = 1.5 * meterScale
meterBoxZ = 0.1 * meterScale
meterBox = box(color = color.white, size = vector(meterBoxX, meterBoxY, meterBoxZ), pos = vector(0, 0.9 * meterBoxY / 2, -meterBoxZ))

# Draw the meter needle and set it to the 0 position.
meterNeedleL = 1.0 * meterScale
meterNeedleW = 0.02 * meterScale
meterNeedle = arrow(length = meterNeedleL, shaftwidth = meterNeedleW, color = color.red, axis = vector(meterNeedleL * np.cos(5 * np.pi / 6), meterNeedleL * np.sin(5 * np.pi / 6), 0))
meterNeedleBaseR = 0.05 * meterScale
meterNeedleBase = sphere(radius = meterNeedleBaseR, color = color.red)

# Place the meter name.
meterName = label(text = "<b>Volts</b>", color = color.red, opacity = 0, box = False, pos = vector(0, (meterNeedleL + 0.25 * meterScale), 0))

# Draw the meter scale major marks.
majTickL = 0.1 * meterScale
majTickW = 0.02 * meterScale
majTickH = 0.02 * meterScale
unitCounter = 0
for theta in np.linspace(5 * np.pi / 6, np.pi / 6, 6):
    majorTick=box(color = color.black, pos = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0), size = vector(majTickL, majTickW, majTickH), axis = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0))
    majorUnit=label(text = str(unitCounter), color = color.red, opacity = 0, box = False, pos = vector((meterNeedleL + 0.15 * meterScale) * np.cos(theta), (meterNeedleL + 0.15 * meterScale) * np.sin(theta), 0))
    unitCounter += 1

# Draw the meter scale minor marks.
minTickL = 0.05 * meterScale
minTickW = 0.01 * meterScale
minTickH = 0.01 * meterScale
for theta in np.linspace(5 * np.pi / 6, np.pi / 6, 51):
    minorTick = box(color = color.black, pos = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0), size = vector(minTickL, minTickW, minTickH), axis = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0))

# Add a raw reading too.
rawValue = label(text = "0000", color = color.red, opacity = 0, box = False, pos = vector(-0.9 * meterScale, (meterNeedleL + 0.25 * meterScale), 0))

# Add a digital reading too.
digitalValue = label(text = "0.00V", color = color.red, opacity = 0, box = False, pos = vector(0.9 * meterScale, (meterNeedleL + 0.25 * meterScale), 0))

# Connect to the Arduino on the correct serial port!
arduinoDataStream = serial.Serial('com3', 115200)
# Give the serial port time to connect.
time.sleep(1)

# An infinite loop...
while True:
    # Wait until data has been received from the Arduino.
    while arduinoDataStream.in_waiting == 0:
        pass
    # Read the data from the Arduino.
    arduinoDataPacket = arduinoDataStream.readline()
    # Convert the data from a byte stream to a string.
    arduinoDataPacket = str(arduinoDataPacket, 'utf-8')
    # Convert the string to a number.
    potValue = int(arduinoDataPacket.strip('\r\n'))
    # Print the raw potentiometer value.
    rawValue.text = str("<i>%04d</i>" % potValue)
    # Print the digital voltage.
    voltage = round(5 * potValue / 1024, 2)
    digitalValue.text = str("%1.2f" % voltage) + "V"
    # Use the potentiometer to set the meter needle angle.
    # How this works:
    #   0V is 5pi/6 rads, 5V is pi/6 rads, thus the needle range is 4pi/6 rads.
    #   The pot range is 0 - 1023, or 1024 steps, so each step is 4pi/6/1024, or pi/1536 rads.
    #   Thus, the needle position is 5pi/6 - (pi/1536 X Potentiometer Value) rads.
    theta = (5 * np.pi / 6) - (np.pi / 1536 * potValue)
    meterNeedle.axis = vector(meterNeedleL * np.cos(theta), meterNeedleL * np.sin(theta), 0)

# EOF
