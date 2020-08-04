import etrobosim.ev3api as ev3
import etrobosim as ets
import time
import math

# まっすぐ進んで、センサ値を表示する。

def dispSensor():
    print("RGB={}".format(colorSensor.getRawColor()))
    print("GYRO_ANGLE={}, ANGLER_VELOCITY={}".format(gyroSensor.getAngle(),gyroSensor.getAnglerVelocity()))

motorR=ev3.Motor(ev3.ePortM.PORT_B,True,ev3.MotorType.LARGE_MOTOR)
motorL=ev3.Motor(ev3.ePortM.PORT_C,True,ev3.MotorType.LARGE_MOTOR)
motorL.setPWM(50)
motorR.setPWM(50)
colorSensor=ev3.ColorSensor(ev3.ePortS.PORT_2)
gyroSensor=ev3.GyroSensor(ev3.ePortS.PORT_4)

try:
    controller=ets.Controller(ets.Course.LEFT)
    controller.addHandlers([motorR,motorL,colorSensor,gyroSensor])
    controller.start(debug=False)
    controller.runCyclic(dispSensor,interval=1.0)
    controller.exit_process()
except KeyboardInterrupt:
    controller.exit_process()
    raise

