import etrobosim.ev3api as ev3
import etrobosim.measurement as mes
import etrobosim as ets
import time
import math

# ColorSensorのReflectを使ってP制御でライントレースする。似非10ms周期

def calcPID(r, target=20, power=70,P=1.8):
    p=r-target
    left=power-P*p
    right=power+P*p
    return (int(left),int(right))

def pidControl(initARM_count=-50,initTAIL_count=0):
    left,right=calcPID(colorSensor.getBrightness())
    motorL.setPWM(left)
    motorR.setPWM(right)
    motorARM.setPWM(initARM_count-motorARM.getCount())
    motorTAIL.setPWM(initTAIL_count-motorTAIL.getCount())
    print(vars(measurement))

motorR=ev3.Motor(ev3.ePortM.PORT_B,True,ev3.MotorType.LARGE_MOTOR)
motorL=ev3.Motor(ev3.ePortM.PORT_C,True,ev3.MotorType.LARGE_MOTOR)
motorARM=ev3.Motor(ev3.ePortM.PORT_A,True,ev3.MotorType.MEDIUM_MOTOR)
motorTAIL=ev3.Motor(ev3.ePortM.PORT_D,True,ev3.MotorType.LARGE_MOTOR)
motorR.reset()
motorL.reset()
colorSensor=ev3.ColorSensor(ev3.ePortS.PORT_2)
gyroSensor=ev3.GyroSensor(ev3.ePortS.PORT_4)
measurement=mes.Measurement()
touchSensor=ev3.TouchSensor(ev3.ePortS.PORT_1)

try:
    controller=ets.Controller(ets.Course.LEFT)
    controller.addHandlers([motorR,motorL,motorARM,motorTAIL,colorSensor,gyroSensor,touchSensor,measurement])
    controller.start(debug=False)
    gyroSensor.reset()
    while (not touchSensor.isPressed()):
        time.sleep(0.1)
    controller.runCyclic(pidControl)
    controller.exit_process()
except KeyboardInterrupt:
    controller.exit_process()
    raise

