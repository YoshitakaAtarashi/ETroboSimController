from ev3api.Motor import Motor, MotorType, ePortM
from ETroboSimController import ETroboSimController
import time

motorR=Motor(ePortM.PORT_B,True,MotorType.LARGE_MOTOR)
motorL=Motor(ePortM.PORT_C,True,MotorType.LARGE_MOTOR)
motorARM=Motor(ePortM.PORT_A,True,MotorType.MEDIUM_MOTOR)
motorTAIL=Motor(ePortM.PORT_D,True,MotorType.LARGE_MOTOR)

walker=[(50,50),(50,0)]
wid=0

motorR.reset()
motorL.reset()

try:
    controller=ETroboSimController()
    controller.addHandler(motorR)
    controller.addHandler(motorL)
    controller.addHandler(motorARM)
    controller.addHandler(motorTAIL)
#    controller.start(debug=True)
    controller.start(debug=False)
    while controller.isAlive():
        motorR.setPWM(walker[wid][0])
        motorL.setPWM(walker[wid][1])
        wid=(wid+1)%len(walker)
        print("MotorR={},MotorL={}".format(motorR.getCount(),motorL.getCount()))
        time.sleep(1)
    controller.exit_process()
except KeyboardInterrupt:
    controller.exit_process()
    raise

