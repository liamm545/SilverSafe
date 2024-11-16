import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DEVICE_INDEX = -1  # 기본 PulseAudio 장치 사용
THRESHOLD_DB = 30  # 데시벨 기준값

def calculate_decibel(data):
    """RMS 값을 통해 데시벨 계산"""
    rms = np.sqrt(np.mean(np.square(data)))
    db = 20 * np.log10(rms) if rms > 0 else 0
    return db

def is_loud(db):
    """데시벨이 30 이상이면 True 반환"""
    return db >= THRESHOLD_DB

def get_microphone_input():
    """마이크 입력을 받아 데시벨을 측정하고, 30 이상이면 True 반환"""
    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            input_device_index=DEVICE_INDEX,
                            frames_per_buffer=CHUNK)

        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
        db = calculate_decibel(data)
        return is_loud(db)

    except Exception as e:
        print(f"에러 발생: {e}")
        return False

    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
