from ev3api.Motor import *

motor=Motor(1,True,MotorType.MEDIUM_MOTOR)
print(motor.type)
print(motor.getCount())

motor.setBrake(True)


motor=Motor(1,True,type_=MotorType.MEDIUM_MOTOR)