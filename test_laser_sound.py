import pytest
import numpy as np
import pygame
import laser_sound
from laser_sound import LaserSound


@pytest.fixture
def laser():
    """Fixture to create a LaserSound instance for testing."""
    return LaserSound()


def test_initialization(laser):
    """Test that LaserSound initializes correctly."""
    assert laser.sample_rate == 44100
    assert laser.duration == 0.1
    assert laser.fade_out_duration == 0.05


def test_generate_laser_sound_default_params(laser):
    """Test laser sound generation with default parameters."""
    sound = laser.generate_laser_sound()
    assert isinstance(sound, pygame.mixer.Sound)

    # Get the sound array
    sound_array = pygame.sndarray.array(sound)
    assert sound_array.shape[1] == 2  # Should be stereo
    assert len(sound_array) > 0  # Should have samples


def test_generate_laser_sound_custom_params(laser):
    """Test laser sound generation with custom parameters."""
    frequency = 880
    volume = 0.3

    sound = laser.generate_laser_sound(frequency=frequency, volume=volume)
    assert isinstance(sound, pygame.mixer.Sound)

    # Get the sound array
    sound_array = pygame.sndarray.array(sound)
    assert sound_array.shape[1] == 2  # Should be stereo
    assert len(sound_array) > 0  # Should have samples


def test_generate_laser_sound_waveform(laser):
    """Test that the generated waveform has the expected characteristics."""
    frequency = 440
    volume = 0.5

    sound = laser.generate_laser_sound(frequency=frequency, volume=volume)
    sound_array = pygame.sndarray.array(sound)

    # Check that the waveform is normalized
    max_amplitude = np.max(np.abs(sound_array))
    assert max_amplitude <= 32767  # 16-bit max value

    # Check that both channels are identical (stereo)
    assert np.array_equal(sound_array[:, 0], sound_array[:, 1])


def test_play_laser(laser, monkeypatch):
    """Test the play_laser method."""

    # Mock pygame.mixer.Sound.play and fadeout methods
    class MockSound:
        def play(self):
            pass

        def fadeout(self, duration):
            pass

    # Mock the generate_laser_sound method to return our mock sound
    def mock_generate(*args, **kwargs):
        return MockSound()

    monkeypatch.setattr(laser, "generate_laser_sound", mock_generate)

    # Test with different parameters
    laser.play_laser(frequency=440, volume=0.5)
    laser.play_laser(frequency=880, volume=0.3)
    laser.play_laser(frequency=220, volume=0.7)


def test_edge_cases(laser):
    """Test edge cases and boundary conditions."""
    # Test with very low frequency
    sound = laser.generate_laser_sound(frequency=20, volume=0.5)
    assert isinstance(sound, pygame.mixer.Sound)

    # Test with very high frequency
    sound = laser.generate_laser_sound(frequency=2000, volume=0.5)
    assert isinstance(sound, pygame.mixer.Sound)

    # Test with minimum volume
    sound = laser.generate_laser_sound(frequency=440, volume=0.0)
    assert isinstance(sound, pygame.mixer.Sound)

    # Test with maximum volume
    sound = laser.generate_laser_sound(frequency=440, volume=1.0)
    assert isinstance(sound, pygame.mixer.Sound)


def test_sound_characteristics(laser):
    """Test that the sound has the expected characteristics."""
    frequency = 440
    volume = 0.5

    sound = laser.generate_laser_sound(frequency=frequency, volume=volume)
    sound_array = pygame.sndarray.array(sound)

    # Check that the sound has a reasonable duration
    expected_samples = int(laser.sample_rate * laser.duration)
    assert len(sound_array) == expected_samples

    # Check that the sound has both positive and negative values
    assert np.any(sound_array > 0)
    assert np.any(sound_array < 0)


def test_main_block(monkeypatch):
    """Test the main block execution."""

    # Mock time.sleep to avoid actual delays
    def mock_sleep(*args):
        pass

    # Mock the play_laser method to verify it's called
    play_calls = []

    def mock_play_laser(self, frequency=440, volume=0.5):
        play_calls.append((frequency, volume))

    # Create a mock LaserSound class
    class MockLaserSound:
        def __init__(self):
            pass

        def play_laser(self, frequency=440, volume=0.5):
            play_calls.append((frequency, volume))

    # Apply mocks
    monkeypatch.setattr("time.sleep", mock_sleep)
    monkeypatch.setattr(laser_sound, "LaserSound", MockLaserSound)

    # Execute the main block
    laser_sound.__name__ = "__main__"
    exec(open("laser_sound.py").read())

    # Verify the expected calls were made
    assert len(play_calls) == 3
    assert play_calls[0] == (880, 0.5)  # High-pitched laser
    assert play_calls[1] == (440, 0.3)  # Medium-pitched laser
    assert play_calls[2] == (220, 0.7)  # Low-pitched laser
