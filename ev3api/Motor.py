
from enum import IntEnum
from struct import pack_into, unpack_from

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
        self.stop_timer = 0

    def reset(self):
        self.brake= True 
        self.count = 0   # ev3_motor_reset_counts(mPort);
        self.offset = 0  

    def getCount(self):
        return self.count-self.offset

    def getPort(self):
        return self.port

    def getPWM(self):
        return self.pwm

    def setCount(self, count : int):
        self.offset = self.count-count

    def setPWM(self, pwm : int):
        self.pwm = min(self.PWM_MAX, max(pwm, self.PWM_MIN))

    def setBrake(self, brake : bool):
        self.brake = brake
    
    def stop(self):
        # (void)ev3_motor_stop(mPort, mBrake); 
        self.stop_timer=3

    def updateData(self, data : bytearray):
        print(36+self.port*4)
        pack_into('<i' ,data,36+self.port*4,self.pwm)
        pack_into('<I' ,data,52+self.port*4,1 if self.brake else 0)
        if self.stop_timer>0:
            self.stop_timer-=1
            st=1
        else:
            st=0
        pack_into('<I' ,data,68+self.port*4,st)
