import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEVICE_INDEX = -1  # Use default PulseAudio device
THRESHOLD_DB = 35  # Decibel threshold


def calculate_decibel(data):
    rms = np.sqrt(np.mean(np.square(data)))
    db = 20 * np.log10(rms) if rms > 0 else 0
    return db


def is_loud(db):
    return db >= THRESHOLD_DB


def get_microphone_input():
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            input_device_index=DEVICE_INDEX,
            frames_per_buffer=CHUNK,
        )

        # Read audio data from the microphone
        data = np.frombuffer(
            stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16
        )

        # Calculate the decibel level
        db = calculate_decibel(data)
        return is_loud(db)

    except Exception as e:
        # Print the error if any occurs
        print(f"Error occurred: {e}")
        return False

    finally:
        # Ensure the stream and audio resources are released
        stream.stop_stream()
        stream.close()
        audio.terminate()
