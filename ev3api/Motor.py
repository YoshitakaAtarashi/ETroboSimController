
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

    def __init__(self, port, brake=True, type_=MotorType.LARGE_MOTOR):
        self.port = port
        self.brake = brake
        self.type = type_
