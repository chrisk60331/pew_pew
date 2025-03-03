import pygame
import numpy as np
import time


class LaserSound:
    """A class that generates and plays laser sound effects."""

    def __init__(self) -> None:
        """Initialize the laser sound generator."""
        # Initialize pygame mixer
        pygame.mixer.init()

        # Sound parameters
        self.sample_rate: int = 44100
        self.duration: float = 0.1  # seconds
        self.fade_out_duration: float = 0.05  # seconds

    def generate_laser_sound(
        self, frequency: float = 440, volume: float = 0.5
    ) -> pygame.mixer.Sound:
        """
        Generate a laser sound with specified frequency and volume.

        Args:
            frequency: The starting frequency of the laser sound in Hz
            volume: Volume level between 0.0 and 1.0

        Returns:
            A pygame Sound object containing the generated laser sound
        """
        # Generate time array
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration))

        # Create frequency sweep (glissando)
        sweep_factor = np.exp(-3 * t)  # Exponential decay
        sweep_freq = frequency * (1 + 2 * sweep_factor)  # Sweep from 3x to 1x

        # Generate the main frequency with sweep
        main_wave = np.sin(2 * np.pi * sweep_freq * t)

        # Add harmonics with sweep
        harmonics = 0.5 * np.sin(2 * np.pi * sweep_freq * 2 * t) + 0.25 * np.sin(
            2 * np.pi * sweep_freq * 3 * t
        )

        # Add a high-pitched "whistle" component
        whistle = 0.3 * np.sin(2 * np.pi * frequency * 8 * t) * sweep_factor

        # Add a low "whoosh" component
        whoosh = 0.2 * np.sin(2 * np.pi * frequency * 0.5 * t) * (1 - sweep_factor)

        # Combine all waves and normalize
        combined_wave = main_wave + harmonics + whistle + whoosh
        combined_wave = combined_wave / np.max(np.abs(combined_wave))

        # Apply volume and envelope
        envelope = np.exp(-5 * t)  # Quick attack, slower decay
        combined_wave = combined_wave * envelope * volume

        # Convert to 16-bit integer and create stereo
        sound_array = np.column_stack((combined_wave, combined_wave))
        sound_array = (sound_array * 32767).astype(np.int16)

        # Create pygame sound object
        sound = pygame.sndarray.make_sound(sound_array)

        return sound

    def play_laser(self, frequency: float = 440, volume: float = 0.5) -> None:
        """
        Generate and play a laser sound.

        Args:
            frequency: The starting frequency of the laser sound in Hz
            volume: Volume level between 0.0 and 1.0
        """
        sound = self.generate_laser_sound(frequency=frequency, volume=volume)
        sound.play()
        time.sleep(self.duration)
        sound.fadeout(int(self.fade_out_duration * 1000))  # fadeout in ms


# Example usage
if __name__ == "__main__":
    laser = LaserSound()

    # Play a few different laser sounds
    print("Playing laser sounds...")
    laser.play_laser(frequency=880, volume=0.5)  # High-pitched laser
    time.sleep(0.5)
    laser.play_laser(frequency=440, volume=0.3)  # Medium-pitched laser
    time.sleep(0.5)
    laser.play_laser(frequency=220, volume=0.7)  # Low-pitched laser
