import serial
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volume.GetMasterVolumeLevel()


arduino = serial.Serial(port='COM3', baudrate=9600, timeout=.1)

def write(x):
    if (x == 0):
        arduino.write(b'1')
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
while True:
    x = round(volume.GetMasterVolumeLevelScalar() * 10)
    write(x)
    vol = (((arduino.readline()).decode()).strip())
    if vol == '':
        continue
    vol = (int(vol)/1000)

    if vol < 0.035:
        vol = 0
    if vol > 1:
        vol = 1
    volume.SetMasterVolumeLevelScalar(vol, None)
    time.sleep(0.01)
