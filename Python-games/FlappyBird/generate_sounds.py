import os
import struct
import wave

import numpy as np


def generate_crash_sound(filename="sounds/crash.wav", duration=0.5, sample_rate=44100):
    """Generate a crash sound effect"""
    # Create sounds directory if it doesn't exist
    os.makedirs("sounds", exist_ok=True)

    num_samples = int(duration * sample_rate)

    # Generate crash sound - combination of noise and descending tone
    t = np.linspace(0, duration, num_samples)

    # White noise for crash effect
    noise = np.random.normal(0, 0.3, num_samples)

    # Descending frequency for impact
    frequency_start = 800
    frequency_end = 100
    frequency = np.linspace(frequency_start, frequency_end, num_samples)
    tone = 0.4 * np.sin(2 * np.pi * frequency * t)

    # Envelope to fade out
    envelope = np.exp(-5 * t)

    # Combine everything
    crash = (noise + tone) * envelope

    # Normalize
    crash = crash / np.max(np.abs(crash))
    crash = (crash * 32767).astype(np.int16)

    # Write to WAV file
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(crash.tobytes())

    print(f"✓ Generated {filename}")


def generate_jump_sound(filename="sounds/jump.wav", duration=0.15, sample_rate=44100):
    """Generate a jump/flap sound effect"""
    os.makedirs("sounds", exist_ok=True)

    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)

    # Rising frequency for jump
    frequency_start = 400
    frequency_end = 800
    frequency = np.linspace(frequency_start, frequency_end, num_samples)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Quick fade envelope
    envelope = np.exp(-10 * t)

    # Apply envelope
    jump = tone * envelope

    # Normalize
    jump = jump / np.max(np.abs(jump))
    jump = (jump * 32767).astype(np.int16)

    # Write to WAV file
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(jump.tobytes())

    print(f"✓ Generated {filename}")


def generate_score_sound(filename="sounds/score.wav", duration=0.2, sample_rate=44100):
    """Generate a score point sound effect"""
    os.makedirs("sounds", exist_ok=True)

    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples)

    # Pleasant chime sound - two notes
    freq1 = 880  # A5
    freq2 = 1320  # E6

    tone1 = 0.3 * np.sin(2 * np.pi * freq1 * t)
    tone2 = 0.3 * np.sin(2 * np.pi * freq2 * t)

    # Envelope
    envelope = np.exp(-8 * t)

    # Combine
    score = (tone1 + tone2) * envelope

    # Normalize
    score = score / np.max(np.abs(score))
    score = (score * 32767).astype(np.int16)

    # Write to WAV file
    with wave.open(filename, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(score.tobytes())

    print(f"✓ Generated {filename}")


if __name__ == "__main__":
    print("Generating sound effects...")
    print()

    try:
        generate_crash_sound()
        generate_jump_sound()
        generate_score_sound()
        print()
        print("✅ All sound effects generated successfully!")
        print("Sound files created in 'sounds/' directory")
    except Exception as e:
        print(f"❌ Error generating sounds: {e}")
        print("Make sure numpy is installed: pip install numpy")
