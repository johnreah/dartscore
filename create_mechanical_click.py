#!/usr/bin/env python3
"""
Generate a mechanical keyboard-style click sound.
This mimics the clacky, sharp sound of mechanical keyboards.
"""
import array
import math
import wave

def generate_mechanical_click():
    """
    Create a mechanical keyboard click sound with:
    - Initial sharp attack (the key hitting)
    - Brief bright resonance
    - Quick decay
    """
    sample_rate = 44100
    duration = 0.08  # 80ms total duration
    
    # Generate time array
    num_samples = int(sample_rate * duration)
    samples = array.array('h')  # 16-bit signed integers
    
    for i in range(num_samples):
        t = i / sample_rate
        
        # Multiple frequency components for realistic mechanical sound
        # High frequency for the "click"
        high_freq = math.sin(2 * math.pi * 3500 * t) * 0.4
        mid_freq = math.sin(2 * math.pi * 2000 * t) * 0.3
        low_freq = math.sin(2 * math.pi * 800 * t) * 0.2
        
        # Add some noise for texture (simulates the mechanical friction)
        import random
        noise = (random.random() - 0.5) * 0.15
        
        # Combine frequencies
        signal = high_freq + mid_freq + low_freq + noise
        
        # Sharp attack envelope (very fast rise, quick decay)
        if t < 0.005:  # First 5ms - sharp attack
            envelope = t / 0.005
        elif t < 0.015:  # Next 10ms - peak
            envelope = 1.0
        else:  # Quick exponential decay
            envelope = math.exp(-40 * (t - 0.015))
        
        # Apply envelope and convert to 16-bit
        sample_value = int(signal * envelope * 32767 * 0.8)
        
        # Clamp to valid 16-bit range
        sample_value = max(-32768, min(32767, sample_value))
        samples.append(sample_value)
    
    # Write to WAV file
    with wave.open('sounds/mechanical_click.wav', 'wb') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)   # 16-bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(samples.tobytes())
    
    print("Mechanical click sound created: sounds/mechanical_click.wav")

if __name__ == '__main__':
    generate_mechanical_click()
