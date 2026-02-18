import os
import re
import csv
import argparse
import numpy as np
import librosa

FPS = 75  # required frames per second


def extract_frequency(filename: str) -> float:
    """
    Extracts frequency from filename of format 'freq-n.wav'
    Example: 440-1.wav -> 440
    """
    match = re.match(r"([0-9]+(?:\.[0-9]+)?)\-", filename)
    if not match:
        raise ValueError(f"Filename does not match expected format: {filename}")
    return float(match.group(1))


def generate_csv_for_audio(audio_path: str):
    directory = os.path.dirname(audio_path)
    filename = os.path.basename(audio_path)
    name, _ = os.path.splitext(filename)

    freq = extract_frequency(filename)

    # Load audio to compute duration
    y, sr = librosa.load(audio_path, sr=None)
    duration_seconds = len(y) / sr

    total_frames = int(np.floor(duration_seconds * FPS))

    csv_path = os.path.join(directory, f"{name}.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pitch"])  # Header must match parameters.json
        
        for _ in range(total_frames):
            writer.writerow([freq])

    print(f"Generated: {csv_path} ({total_frames} frames)")


def process_folder(folder_path: str):
    supported_formats = (
        ".wav", ".mp3", ".flac", ".aac", ".ogg", ".m4a",
        ".wma", ".aiff", ".au", ".ra", ".3gp",
        ".amr", ".ac3", ".dts", ".ape", ".mka", ".opus"
    )

    for file in os.listdir(folder_path):
        if file.lower().endswith(supported_formats):
            audio_path = os.path.join(folder_path, file)
            generate_csv_for_audio(audio_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate 75 FPS annotation CSV files for frequency-based audio dataset.")
    parser.add_argument("folder", type=str, help="Path to folder containing audio files")
    args = parser.parse_args()

    process_folder(args.folder)
