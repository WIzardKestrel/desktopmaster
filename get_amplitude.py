import struct
import numpy as np
import pyaudio
import wave
from scipy.fftpack import fft
import matplotlib.pyplot as plt
def ave(k):
    sum = 0
    for i in k:
        sum += i
    sum = round((1000 * (sum/len(k))))
    return sum
CHUNK = 1024 * 2
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()

#SPEAKERS = p.get_device_info_by_index(5) #The part I have modified
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if (dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0):
        dev_index = dev['index']
        print('dev_index', dev_index)

print(p.get_default_output_device_info()["index"],p.get_default_output_device_info()["name"])
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=dev_index) #The part I have modified

print("* recording")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    #k = np.array(struct.unpack(str(2 * CHUNK) + 'B', data))[::2] + 127
    k = np.array(struct.unpack(str(2 * CHUNK) + 'B', data))[::2]
    frames.append(data)
    amp = np.linspace(0, RATE, CHUNK)
    y_amp = np.abs(fft(k)[0:CHUNK] * 2 / (256 * CHUNK))
    print(ave(y_amp[100:1000]))
    print("new y_amp")
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
