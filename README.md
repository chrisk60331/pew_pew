# Laser Sound Generator

A Python class that generates authentic "pew pew" laser sound effects using pygame and numpy. Perfect for games, interactive applications, or just having fun with sci-fi sound effects!

## Features

- Generates realistic laser sound effects with:
  - Frequency sweep (glissando) for the classic "pew" effect
  - High-pitched "whistle" component
  - Low "whoosh" component
  - Quick attack and natural decay
- Fully customizable parameters:
  - Frequency (pitch)
  - Volume
  - Duration
  - Fade-out ratio
- Stereo audio output
- Easy to use API
- Duration control for different laser types:
  - Quick zaps
  - Standard laser shots
  - Long laser beams

## Installation

1. Clone this repository or download the files
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```python
from laser_sound import LaserSound

# Create a laser sound generator
laser = LaserSound()

# Play a standard laser sound
laser.play_laser(frequency=440, volume=0.5)
```

### Parameters

- `frequency` (float): The starting frequency of the laser sound in Hz
  - Higher values (e.g., 880) create higher-pitched lasers
  - Lower values (e.g., 220) create lower-pitched lasers
- `volume` (float): Volume level between 0.0 and 1.0
- `duration` (float, optional): Duration of the sound in seconds
  - Default: 0.1 seconds
  - Shorter durations (e.g., 0.05) create quick zaps
  - Longer durations (e.g., 0.3) create sustained laser beams

### Examples

```python
# Create different types of laser sounds
laser = LaserSound()

# Quick zap (0.05 seconds)
laser.play_laser(frequency=880, volume=0.5, duration=0.05)

# Standard laser shot (0.1 seconds)
laser.play_laser(frequency=440, volume=0.3)

# Long laser beam (0.3 seconds)
laser.play_laser(frequency=220, volume=0.7, duration=0.3)
```

### Advanced Usage

You can also generate the sound without playing it:
```python
# Generate a laser sound
sound = laser.generate_laser_sound(
    frequency=440,
    volume=0.5,
    duration=0.2
)

# Play it later
sound.play()
```

## Sound Components

The laser sound is composed of several components that create a rich, sci-fi effect:

1. **Main Frequency**: The base tone of the laser
2. **Frequency Sweep**: Creates the "pew" effect by sliding from high to low
3. **Harmonics**: Adds richness to the sound
4. **Whistle**: High-frequency component for that laser "zing"
5. **Whoosh**: Low-frequency component for added presence

All components automatically scale with the duration while maintaining their relative timing relationships.

## Requirements

- Python 3.x
- pygame
- numpy

## Development

This project uses several development tools:
- pytest for testing
- coverage for test coverage
- pre-commit hooks for code quality
- ruff and pylint for linting
- mypy for type checking

To set up the development environment:
```bash
pip install -r requirements.txt
pre-commit install
```

## License

This project is open source and available under the MIT License. 