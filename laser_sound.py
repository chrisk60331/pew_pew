import pygame
import numpy as np
import time
from typing import Optional


class LaserSound:
    """A class that generates and plays laser sound effects."""

    def __init__(self) -> None:
        """Initialize the laser sound generator."""
        # Initialize pygame mixer
        pygame.mixer.init()

        # Sound parameters
        self.sample_rate: int = 44100
        self.default_duration: float = 0.1  # seconds
        self.fade_ratio: float = 0.5  # ratio of duration for fade out

    def generate_laser_sound(
        self,
        frequency: float = 440,
        volume: float = 0.5,
        duration: Optional[float] = None
    ) -> pygame.mixer.Sound:
        """
        Generate a laser sound with specified parameters.

        Args:
            frequency: The starting frequency of the laser sound in Hz
            volume: Volume level between 0.0 and 1.0
            duration: Duration of the sound in seconds (default: 0.1)

        Returns:
            A pygame Sound object containing the generated laser sound
        """
        # Use default duration if none provided
        sound_duration = duration if duration is not None else self.default_duration

        # Generate time array
        t = np.linspace(0, sound_duration, int(self.sample_rate * sound_duration))

        # Create frequency sweep (glissando)
        sweep_factor = np.exp(-3 * t / sound_duration)  # Scale decay with duration
        sweep_freq = frequency * (1 + 2 * sweep_factor)  # Sweep from 3x to 1x

        # Generate the main frequency with sweep
        main_wave = np.sin(2 * np.pi * sweep_freq * t)

        # Add harmonics with sweep
        harmonics = (
            0.5 * np.sin(2 * np.pi * sweep_freq * 2 * t) +
            0.25 * np.sin(2 * np.pi * sweep_freq * 3 * t)
        )

        # Add a high-pitched "whistle" component
        whistle = (
            0.3 * np.sin(2 * np.pi * frequency * 8 * t) * sweep_factor
        )

        # Add a low "whoosh" component
        whoosh = (
            0.2 * np.sin(2 * np.pi * frequency * 0.5 * t) * (1 - sweep_factor)
        )

        # Combine all waves and normalize
        combined_wave = main_wave + harmonics + whistle + whoosh
        combined_wave = combined_wave / np.max(np.abs(combined_wave))

        # Apply volume and envelope
        envelope = np.exp(-5 * t / sound_duration)  # Scale decay with duration
        combined_wave = combined_wave * envelope * volume

        # Convert to 16-bit integer and create stereo
        sound_array = np.column_stack((combined_wave, combined_wave))
        sound_array = (sound_array * 32767).astype(np.int16)

        # Create pygame sound object
        sound = pygame.sndarray.make_sound(sound_array)

        return sound

    def play_laser(
        self,
        frequency: float = 440,
        volume: float = 0.5,
        duration: Optional[float] = None
    ) -> None:
        """
        Generate and play a laser sound.

        Args:
            frequency: The starting frequency of the laser sound in Hz
            volume: Volume level between 0.0 and 1.0
            duration: Duration of the sound in seconds (default: 0.1)
        """
        # Use default duration if none provided
        sound_duration = duration if duration is not None else self.default_duration
        fade_duration = sound_duration * self.fade_ratio

        sound = self.generate_laser_sound(
            frequency=frequency,
            volume=volume,
            duration=sound_duration
        )
        sound.play()
        time.sleep(sound_duration)
        sound.fadeout(int(fade_duration * 1000))  # fadeout in ms


# Example usage
if __name__ == "__main__":
    laser = LaserSound()

    # Play a few different laser sounds with varying durations
    print("Playing laser sounds...")

    # Quick zap (0.05 seconds)
    laser.play_laser(frequency=880, volume=0.5, duration=0.5)
    time.sleep(0.5)

    # Standard laser (0.1 seconds)
    laser.play_laser(frequency=440, volume=0.3)
    time.sleep(0.5)

    # Long laser beam (0.3 seconds)
    laser.play_laser(frequency=220, volume=0.7, duration=0.3)
