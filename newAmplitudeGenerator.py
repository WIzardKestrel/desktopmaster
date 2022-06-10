import struct
import numpy as np
import pyaudio
import wave
from scipy.fftpack import fft
import serial
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math

def ave(k):
    s = sum(k)
    s = round((s/len(k)))
    return s
CHUNK = 64 * 2 #1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
maxValue = 2**16

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



#
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     #k = np.array(struct.unpack(str(2 * CHUNK) + 'B', data))[::2] + 127
#     k = np.array(struct.unpack(str(2 * CHUNK) + 'B', data))[::2]
#     #frames.append(data)
#     amp = np.linspace(0, RATE, CHUNK)
#     y_amp = np.abs(fft(k)[0:CHUNK] * 2 / (256 * CHUNK))
#


arduino = serial.Serial(port='COM3', baudrate=9600, timeout=0)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMasterVolumeLevel()


def write(x):
    if (x == 0):
        arduino.write(b'0')
    if (x == 1):
      arduino.write(b'1')
    if (x == 2):
      arduino.write(b'2')
    if (x == 3):
      arduino.write(b'3')
    if (x == 4):
      arduino.write(b'4')
    if (x == 5):
        arduino.write(b'5')
    if (x == 6):
        arduino.write(b'6')
    if (x == 7):
        arduino.write(b'7')
    if (x == 8):
        arduino.write(b'8')
    if (x == 9):
        arduino.write(b'9')
    if (x == 10):
        arduino.write(b'10')


def write_amplitude(a):
    pass


# def correct(a):
#     return round(0.8 * a)
old_amp = 0
o1 = 0
o2 = 0
o3 = 0
count = 0
x_old = 0
def largestIndexMax(amplitudes):
    pass

maxValue = 2**16
bars = 10
while True:
    data = np.abs(np.frombuffer(stream.read(1024), dtype=np.int16))

    # for i in range(len(normalized)):
    #     if normalized[i] < 1:
    #         continue
    #     normalized[i] = math.log(normalized[i], 2)
    # scale = 9 - ave(normalized)
    #scale = (9 - math.log(ave(data)))
    peak = (int)(10 * bars * np.abs(np.max(data) - np.min(data)) / maxValue)

    # lS = "#" * (peak * bars) + "-" * (bars - peak * bars)
   # print("L=[%s]" % (lS))
    # vol = (((arduino.readline()).decode()).strip())
    # x = round(volume.GetMasterVolumeLevelScalar() * 10)
    # if(x != x_old):
    #     x_old = x
    #     write(x)

    # write(correct(amplitude))

    write(peak)
    print(peak)

    # if vol == '':
    #     continue
    # vol = (int(vol)/1000)
    # if vol < 0.035:
    #     vol = 0
    # if vol > 1:
    #     vol = 1
    #
    # volume.SetMasterVolumeLevelScalar(vol, None)



stream.stop_stream()
stream.close()
p.terminate()
