from struct import pack_into, unpack_from
import threading
from . import ePortS

class SonarSensor:

    def __init__(self, port : ePortS):
        self.port = port
        self.distance = 0
        self.listen_ = 0
        self.lock = threading.Lock()

    def listen(self):
        with self.lock:
            v=self.listen_
        return v!=0

    def getDistance(self):
        with self.lock:
            v=self.distance
        return v

    def _recieveData(self, data : bytearray):
        distance,listen=unpack_from('<ii',data,120)
        with self.lock:
            self.distance=distance
            self.listen_=listen
