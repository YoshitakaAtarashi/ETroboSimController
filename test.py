import etrobosim.ev3api as ev3
import etrobosim as ets
import time
import math


def calcPID(r, target=20, power=70,P=1.8):
    p=r-target
    left=power-P*p
    right=power+P*p
    return (int(left),int(right))


motorR=ev3.Motor(ev3.ePortM.PORT_B,True,ev3.MotorType.LARGE_MOTOR)
motorL=ev3.Motor(ev3.ePortM.PORT_C,True,ev3.MotorType.LARGE_MOTOR)
motorARM=ev3.Motor(ev3.ePortM.PORT_A,True,ev3.MotorType.MEDIUM_MOTOR)
motorTAIL=ev3.Motor(ev3.ePortM.PORT_D,True,ev3.MotorType.LARGE_MOTOR)
motorR.reset()
motorL.reset()
colorSensor=ev3.ColorSensor(ev3.ePortS.PORT_2)
initARM_count=-50
initTAIL_count=0

try:
    controller=ets.Controller(ets.Course.LEFT)
    controller.add(motorR)
    controller.add(motorL)
    controller.add(motorARM)
    controller.add(motorTAIL)
    controller.add(colorSensor)
    controller.start(debug=False)
    while controller.isAlive():
        left,right=calcPID(colorSensor.getBrightness())
        motorL.setPWM(left)
        motorR.setPWM(right)
        motorARM.setPWM(initARM_count-motorARM.getCount())
        motorTAIL.setPWM(initTAIL_count-motorTAIL.getCount())
        print("MotorR={},MotorL={},MotorARM={},Color={}".format(motorR.getCount(),motorL.getCount(),motorARM.getCount(),colorSensor.getBrightness()))
        time.sleep(0.01)
    controller.exit_process()
except KeyboardInterrupt:
    controller.exit_process()
    raise

