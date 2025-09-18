# LED-temperature-interface
This project provides an LED-based temperature interface for a dilution refrigerator using a Model 372 AC Resistance Bridge. The interface displays live temperature readings on an LED strip, providing quick and intuitive visual feedback.

## Features
- Real-time temperature monitoring via Python.  
- LED visualization using Arduino.  
- Color-coded display to represent temperature ranges.  
- Compatible with Model 372 AC Resistance Bridge.

## Hardware
- Arduino-compatible board (I used an Arduino Uno)
- Addressable LED strip (I used WS2812)
- Model 372 AC Resistance Bridge

## Software
- Arduino IDE
- Python 3.11 or lower (so3g only runs on Python 3.11 or lower)
- Jupyter Notebook

### Requires the following repositories:
- https://github.com/simonsobs/so3g
- https://github.com/ceres-solver/ceres-solver
- https://www.gnu.org/software/gsl/
- https://github.com/abseil/abseil-cpp
- https://github.com/pyserial/pyserial
- https://github.com/numpy/numpy

### In Arduino, include:
- FastLED library: https://github.com/FastLED/FastLED

## Files
### ArduinoScript
Arduino sketch to control LED strip based on the signals received from the Python script. It flashes when condensing begins. The colour range is as follows:
- Above 273.15 K: White (no colour change)
- 273.15 K: Red, fading into
- 200 K: Orange, fading into
- 100 K: Yellow, fading into
- 40 K: Green, fading into
- 10 K: Cyan, fading into
- 4 K: Blue, fading into
- 0.01 K: Purple

### Python Script
Python script to grab temperature from the Model 372 AC Resistance Bridge. It switches channels (thermometers) based on which stage of cooldown the dilution refrigerator is at.

A lot of my code is taken from Lawrence Lin's thermometer calibration code, which you can check out here: https://github.com/LawrenceTLin/NiemackLab/tree/main/Therm_cal
