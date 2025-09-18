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

## Files
- ArduinoScript --> Arduino sketch to control LED strip
- 

A lot of my code is taken from Lawrence Lin's thermometer calibration code, which you can check out here: https://github.com/LawrenceTLin/NiemackLab/tree/main/Therm_cal
