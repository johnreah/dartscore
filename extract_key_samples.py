#!/usr/bin/env python3
"""
Extract individual key press samples from a typing sound recording.
"""
import wave
import array
import os

def extract_key_samples():
    """
    Extract multiple key press samples from the typing audio file.
    Detects individual key presses and saves them as separate files.
    """
    # Read the source audio file
    with wave.open(os.path.expanduser('~/Desktop/typing-18347.wav'), 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        num_frames = wav_file.getnframes()
        
        print(f"Sample rate: {sample_rate} Hz")
        print(f"Channels: {num_channels}")
        print(f"Sample width: {sample_width} bytes")
        print(f"Duration: {num_frames / sample_rate:.2f} seconds")
        
        # Read all audio data
        audio_data = wav_file.readframes(num_frames)
        
        # Convert to array of integers
        if sample_width == 2:  # 16-bit
            samples = array.array('h', audio_data)  # signed short
        else:
            print(f"Unsupported sample width: {sample_width}")
            return
        
        # If stereo, convert to mono by averaging channels
        if num_channels == 2:
            mono_samples = array.array('h')
            for i in range(0, len(samples), 2):
                avg = (samples[i] + samples[i+1]) // 2
                mono_samples.append(avg)
            samples = mono_samples
        
        print(f"Total samples: {len(samples)}")
        
        # Find key press events by detecting peaks
        threshold = max(abs(max(samples)), abs(min(samples))) * 0.15  # 15% of max amplitude
        min_silence = int(sample_rate * 0.05)  # 50ms minimum between key presses
        key_sample_length = int(sample_rate * 0.10)  # 100ms per key sample
        
        key_presses = []
        i = 0
        while i < len(samples):
            # Look for peak above threshold
            if abs(samples[i]) > threshold:
                # Found a key press - extract sample
                start = max(0, i - int(sample_rate * 0.005))  # Start 5ms before peak
                end = min(len(samples), start + key_sample_length)
                
                key_sample = samples[start:end]
                key_presses.append(key_sample)
                
                # Skip ahead to avoid detecting same key press multiple times
                i += min_silence
                
                # Limit to 10 samples
                if len(key_presses) >= 10:
                    break
            else:
                i += 1
        
        print(f"Extracted {len(key_presses)} key press samples")
        
        # Save the extracted samples
        os.makedirs('sounds', exist_ok=True)
        
        for idx, key_sample in enumerate(key_presses):
            filename = f'sounds/key_sample_{idx + 1}.wav'
            with wave.open(filename, 'wb') as out_file:
                out_file.setnchannels(1)
                out_file.setsampwidth(2)
                out_file.setframerate(sample_rate)
                out_file.writeframes(key_sample.tobytes())
            print(f"Saved: {filename}")
        
        # Also save the first one as the default mechanical_click.wav
        if key_presses:
            with wave.open('sounds/mechanical_click.wav', 'wb') as out_file:
                out_file.setnchannels(1)
                out_file.setsampwidth(2)
                out_file.setframerate(sample_rate)
                out_file.writeframes(key_presses[0].tobytes())
            print("Saved default: sounds/mechanical_click.wav")

if __name__ == '__main__':
    extract_key_samples()
