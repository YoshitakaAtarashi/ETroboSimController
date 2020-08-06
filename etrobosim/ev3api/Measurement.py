from struct import pack_into, unpack_from
import threading

# 計測システム連携テスト用
class Measurement:

    def __init__(self):
        self.isStart=False        
        self.cardNumber=0
        self.blockNumber=0
        self.adv_layout=''
        self.measurement_time=0.0
        self.run_time=0.0
        self.lock = threading.Lock()

    def getCardNumber(self):
        with self.lock:
            v=self.cardNumber
        return v

    def getBlockNumber(self):
        with self.lock:
            v=self.blockNumber
        return v

    def getAdvLayout(self):
        with self.lock:
            v=self.adv_layout
        return v



    def _recieveData(self, data : bytearray):
        cardNumber,blockNumber,adv_layout=unpack_from('<ii10s',data,512)
        measurement_time,run_time=unpack_from('<ii',data,532)
        with self.lock:
            self.cardNumber=cardNumber
            self.blockNumber=blockNumber
            self.adv_layout=adv_layout
            self.measurement_time=float(measurement_time)/1000.0
            self.run_time=float(run_time)/1000.0
