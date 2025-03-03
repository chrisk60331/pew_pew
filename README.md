# Laser Sound Generator

A Python class that generates authentic "pew pew" laser sound effects using pygame and numpy. Perfect for games, interactive applications, or just having fun with sci-fi sound effects!

## Features

- Generates realistic laser sound effects with:
  - Frequency sweep (glissando) for the classic "pew" effect
  - High-pitched "whistle" component
  - Low "whoosh" component
  - Quick attack and natural decay
- Adjustable parameters:
  - Frequency (pitch)
  - Volume
  - Duration
  - Fade-out duration
- Stereo audio output
- Easy to use API

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```python
from laser_sound import LaserSound

# Create a laser sound generator
laser = LaserSound()

# Play a laser sound
laser.play_laser(frequency=440, volume=0.5)
```

### Parameters

- `frequency` (float): The starting frequency of the laser sound in Hz
  - Higher values (e.g., 880) create higher-pitched lasers
  - Lower values (e.g., 220) create lower-pitched lasers
- `volume` (float): Volume level between 0.0 and 1.0

### Example

```python
# Create different types of laser sounds
laser = LaserSound()

# High-pitched laser
laser.play_laser(frequency=880, volume=0.5)

# Medium-pitched laser
laser.play_laser(frequency=440, volume=0.3)

# Low-pitched laser
laser.play_laser(frequency=220, volume=0.7)
```

## Requirements

- Python 3.x
- pygame
- numpy

## License

This project is open source and available under the MIT License. 