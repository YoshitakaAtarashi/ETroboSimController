from ev3api.Motor import *
from hexdump import hexdump
from ETroboSimController import *

motor=Motor(ePortM.PORT_B,True,MotorType.LARGE_MOTOR)
print(motor.type)
print(motor.getCount())

motor.setBrake(True)


print(len(ePortM)) # NUM_PORT_M

motor.setPWM(50)
print(motor.pwm)
motor.stop()

data= bytearray(128)
motor.updateDataOfClient(data)
print(hexdump(data))


motorR=Motor(ePortM.PORT_B,True,MotorType.LARGE_MOTOR)
motorL=Motor(ePortM.PORT_C,True,MotorType.LARGE_MOTOR)
motorR.setPWM(50)
motorL.setPWM(50)
motorARM=Motor(ePortM.PORT_A,True,MotorType.MEDIUM_MOTOR)
motorTAIL=Motor(ePortM.PORT_D,True,MotorType.LARGE_MOTOR)

walker=[(50,50),(50,0)]
wid=0

try:
    controller=ETroboSimController()
    controller.client.addHandler(motorR)
    controller.client.addHandler(motorL)
    controller.client.addHandler(motorARM)
    controller.client.addHandler(motorTAIL)
    controller.start(debug=True)
    while controller.isAlive():
        motorR.setPWM(walker[wid][0])
        motorL.setPWM(walker[wid][1])
        wid=(wid+1)%len(walker)
        time.sleep(1)
    controller.exit_process()
except KeyboardInterrupt:
    controller.exit_process()
    raise

