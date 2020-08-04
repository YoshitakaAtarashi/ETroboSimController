
from enum import IntEnum
from struct import pack_into, unpack_from
import threading

class MotorType(IntEnum):
    NONE_MOTOR = 0
    MEDIUM_MOTOR = 1
    LARGE_MOTOR = 2
    UNREGULATED_MOTOR = 3
    TNUM_MOTOR_TYPE = 4

class ePortM(IntEnum):
    PORT_A = 0
    PORT_B = 1 
    PORT_C = 2
    PORT_D = 3

class Motor:
    PWM_MAX = 100
    PWM_MIN = -100

    def __init__(self, port : ePortM, brake : bool = True, type_ : MotorType = MotorType.LARGE_MOTOR):
        self.port = port
        self.brake = brake
        self.type = type_
        self.count = 0
        self.offset = 0
        self.pwm = 0
        self.reset_timer = 0
        self.lock = threading.Lock()
        self.lock2 = threading.Lock()

    def reset(self):
        with self.lock:
            self.brake= True 
            self.offset = 0  
            self.reset_timer = 3

    def getCount(self):
        with self.lock2:
            v=self.count-self.offset
        return v

    def getPort(self):
        return self.port

    def getPWM(self):
        return self.pwm

    def setCount(self, count : int):
        with self.lock2:
            self.offset = self.count-count

    def setPWM(self, pwm : int):
        p=min(self.PWM_MAX, max(pwm, self.PWM_MIN))
        with self.lock:
            self.pwm = p

    def setBrake(self, brake : bool):
        with self.lock:
            self.brake = brake
    
    def stop(self):
        with self.lock:
            self.pwm = 0
            self.brake = True

    def _sendData(self, data : bytearray):
        with self.lock:
            pwm=self.pwm
            brake=1 if self.brake else 0
            if self.reset_timer>0:
                self.reset_timer-=1
                reset=1
            else:
                reset=0            
        pack_into('<i' ,data,36+self.port*4,pwm)
        pack_into('<I' ,data,52+self.port*4,brake)
        pack_into('<I' ,data,68+self.port*4,reset)

    def _recieveData(self, data : bytearray):
        v,=unpack_from('<i',data,288+self.port*4)
        with self.lock2:
            self.count=v
