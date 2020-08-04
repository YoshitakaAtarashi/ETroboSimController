from struct import pack_into, unpack_from
import threading
from . import ePortS

class ColorSensor:
    PWM_MAX = 100
    PWM_MIN = -100

    def __init__(self, port : ePortS):
        self.port = port
        self.ambient=0
        self.color=0
        self.reflect = 0
        self.lock = threading.Lock()

    def getBrightness(self):
        with self.lock:
            v=self.reflect
        return v

    def getColorNumber(self):
        with self.lock:
            v=self.color
        return v

    def getAmbient(self):
        with self.lock:
            v=self.ambient
        return v

    def _recieveData(self, data : bytearray):
        ambient,color,reflect=unpack_from('<iii',data,36)
        with self.lock:
            self.ambient=ambient
            self.color=color
            self.reflect=reflect
