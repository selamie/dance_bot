import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import random


def analyze_audio(audio_path, plot = False):
    y, sr = librosa.load(audio_path, sr=None)

    # Determine a random 30-second segment within the audio duration
    duration = librosa.get_duration(y=y, sr=sr)
    if duration > 30:
        start_time = random.uniform(0, (duration - duration/3))
        end_time = start_time + 30
        print(f"Selected segment: {start_time:.2f}s to {end_time:.2f}s")
        
        # Trim the audio to this segment
        y = y[int(start_time * sr):int(end_time * sr)]
    else:
        print("Audio is shorter than 30 seconds; using full duration.")
        start_time, end_time = 0, duration

    # Onset detection
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='time', backtrack=False, pre_max=20, post_max=20, pre_avg=50, post_avg=50, delta=0.2)
    # Plot onset strength
    if plot:
        plt.figure(figsize=(10, 4))
        librosa.display.waveshow(y, sr=sr, alpha=0.5)
        plt.vlines(onset_frames, -1, 1, color="r", linestyle="dashed", label="Onsets")
        plt.title("Onset Detection")
        plt.legend()
        plt.show()

        # Print detected onset times
        print("Detected Onsets (seconds):")
        print(onset_frames)
        print(f"start time: {start_time}, end: {end_time}")
    
    timestamps = [round(frame, 2) for frame in onset_frames]

    timing = (start_time, end_time)
    return timestamps, timing 

def format_time(secs):
    minutes = secs // 60
    seconds = secs % 60
    if seconds < 10: 
        return f"{int(minutes)}:0{int(seconds)}" 

    return f"{int(minutes)}:{int(seconds)}" 

if __name__ == '__main__':
    audio_path = "skutababa.mp3"  # Replace with your file
    timestamps, timing = analyze_audio(audio_path, plot = True)
    print(format_time(timing[0]), " ", format_time(timing[1]))