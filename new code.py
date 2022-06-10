import math
import time
import serial.tools.list_ports
import pyaudio
import serial
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
CHUNK = 1024  # 1024
CHANNELS = 1
RATE = 44100

com_port = ''

ports = list(serial.tools.list_ports.comports())
for h in ports:
    h = str(h).split(' ')
    com_port = h[0]
    print("connected @ port ", com_port)

p = pyaudio.PyAudio()
# dev = p.get_default_output_device_info()
dev_index = 2
k = p.get_default_output_device_info()["index"]
for i in range(p.get_device_count()):
    dev = p.get_device_info_by_index(i)
    if dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev[
        'hostApi'] == 0:  # TODO: fix this such that it works with any output device
        dev_index = dev['index']
        print('device index', dev_index, 'device name', dev['name'])

stream = p.open(format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=dev_index)

#
# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     data = stream.read(CHUNK)
#     #k = np.array(struct.unpack(str(2 * CHUNK) + 'B', data))[::2] + 127
#     k = np.array(struct.unpack(str(2 * CHUNK) + 'B', data))[::2]
#     #frames.append(data)
#     amp = np.linspace(0, RATE, CHUNK)
#     y_amp = np.abs(fft(k)[0:CHUNK] * 2 / (256 * CHUNK))
#


arduino = serial.Serial(port=com_port, baudrate=9600, timeout=0)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume.iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMasterVolumeLevel()


def write(level):
    if level == 0:
        arduino.write(b'0')
    if level == 1:
        arduino.write(b'1')
    if level == 2:
        arduino.write(b'2')
    if level == 3:
        arduino.write(b'3')
    if level == 4:
        arduino.write(b'4')
    if level == 5:
        arduino.write(b'5')
    if level == 6:
        arduino.write(b'6')
    if level == 7:
        arduino.write(b'7')
    if level == 8:
        arduino.write(b'8')
    if level == 9:
        arduino.write(b'9')
    if level >= 10:
        arduino.write(b':')  # ascii code for ':' is 58, 58 - 48 is 10


while True:

    x = ((volume.GetMasterVolumeLevelScalar()) * 6.5) + 0.01

    data = np.abs(np.frombuffer(stream.read(1024), dtype=np.int16))
    peak = round(((math.sqrt(sum(data) / len(data))) / x))
    # print(peak)
    if volume.GetMasterVolumeLevelScalar() == 0:
        peak = 0

    if peak > 10:
        peak = 10
    # volume.SetMasterVolumeLevelScalar(i, None)

    write(peak)

    vol = (((arduino.readline()).decode()).strip())
    if vol == '':
        continue
    vol = (int(vol) / 1000)
    if vol < 0.035:
        vol = 0
    if vol > 1:
        vol = 1

    volume.SetMasterVolumeLevelScalar(vol, None)
time.sleep(2)
