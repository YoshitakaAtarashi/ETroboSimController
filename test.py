import etrobosim.ev3api as ev3
import etrobosim as ets
import time

motorR=ev3.Motor(ev3.ePortM.PORT_B,True,ev3.MotorType.LARGE_MOTOR)
motorL=ev3.Motor(ev3.ePortM.PORT_C,True,ev3.MotorType.LARGE_MOTOR)
motorARM=ev3.Motor(ev3.ePortM.PORT_A,True,ev3.MotorType.MEDIUM_MOTOR)
motorTAIL=ev3.Motor(ev3.ePortM.PORT_D,True,ev3.MotorType.LARGE_MOTOR)
motorR.reset()
motorL.reset()

walker=[(50,50),(50,0)]
wid=0

try:
    controller=ets.Controller(ets.Course.LEFT)
    controller.add(motorR)
    controller.add(motorL)
    controller.add(motorARM)
    controller.add(motorTAIL)
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

