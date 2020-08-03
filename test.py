from ev3api.Motor import *
from hexdump import hexdump

motor=Motor(ePortM.PORT_B,True,MotorType.LARGE_MOTOR)
print(motor.type)
print(motor.getCount())

motor.setBrake(True)


print(len(ePortM)) # NUM_PORT_M

motor.setPWM(50)
print(motor.pwm)
motor.stop()

data= bytearray(128)
motor.updateData(data)
print(hexdump(data))

