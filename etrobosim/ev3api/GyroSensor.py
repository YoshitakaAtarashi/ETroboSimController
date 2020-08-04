from enum import IntEnum
from struct import pack_into, unpack_from
import threading
from . import ePortS

class GyroSensor:
    DEFAULT_OFFSET = 0

    def __init__(self, port : ePortS):
        self.port = port
        self.reset_timer = 0
        self.angle = 0  
        self.anglerVelocity = 0  
        self.offset = 0  
        self.lock = threading.Lock()
        self.lock2 = threading.Lock()

    def reset(self):
        with self.lock:
            self.angle = 0  
            self.anglerVelocity = 0  
            self.offset = 0  
            self.reset_timer = 3

    def getPort(self):
        return self.port

    def getAngle(self):
        with self.lock2:
            v=self.angle
        return v

    def getAnglerVelocity(self):
        with self.lock2:
            v=self.anglerVelocity-self.offset
        return v

    def setOffset(self, offset : int):
        self.offset =min(1023, max(offset, 0))

    def _sendData(self, data : bytearray):
        with self.lock:
            if self.reset_timer>0:
                self.reset_timer-=1
                reset=1
            else:
                reset=0            
        pack_into('<i' ,data,84,reset)

    def _recieveData(self, data : bytearray):
        angle,anglerVelocity=unpack_from('<ii',data,60)
        with self.lock2:
            self.angle=angle
            self.anglerVelocity=anglerVelocity
