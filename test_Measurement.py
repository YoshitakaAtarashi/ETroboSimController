import etrobosim.ev3api as ev3
import etrobosim.measurement as mes
import etrobosim as ets
import time
import math

# 手動で動かした後、少し待ってから計測データを受け取って終わる。

measurement=mes.Measurement()

try:
    controller=ets.Controller(ets.Course.LEFT)
    controller.addHandlers([measurement])
    controller.start(debug=False)
    time.sleep(0.2)
    print(vars(measurement))
    controller.exit_process()
except KeyboardInterrupt:
    controller.exit_process()
    raise

