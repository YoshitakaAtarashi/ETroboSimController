from struct import pack_into, unpack_from
import threading
from . import ePortS

class TouchSensor:

    def __init__(self, port : ePortS):
        self.port = port
        self.touch = 0
        self.lock = threading.Lock()

    def isPressed(self):
        with self.lock:
            v=self.touch
        return v>=2048

    def _recieveData(self, data : bytearray):
        touch,=unpack_from('<i',data,144)
        with self.lock:
            self.touch=touch