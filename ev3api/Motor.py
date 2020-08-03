
from enum import IntEnum

class MotorType(IntEnum):
    NONE_MOTOR = 0
    MEDIUM_MOTOR = 1
    LARGE_MOTOR = 2
    UNREGULATED_MOTOR = 3
    TNUM_MOTOR_TYPE = 4

class Motor:
    PWM_MAX = 100
    PWM_MIN = -100

    def __init__(self, port, brake : bool = True, type_ : MotorType = MotorType.LARGE_MOTOR):
        self.port = port
        self.brake = brake
        self.type = type_
        self.count = 0
        self.offset = 0
        self.pwm = 0

    def reset(self):
        self.brake= True 
        self.count = 0   # ev3_motor_reset_counts(mPort);
        self.offset = 0  

    def getCount(self):
        return self.count-self.offset

    def setCount(self, count : int):
        self.offset = self.count-count

    def setPWM(self, pwm : int):
        self.pwm = pwm 

    def setBrake(self, brake : bool):
        self.brake = brake
    

