from struct import pack_into, unpack_from
import threading

# 計測システム連携テスト用
class Measurement:

    def __init__(self):
        self.cardNumber=0
        self.blockNumber=0
        self.adv_layout=''
        self.measurement_time=0.0
        self.run_time=0.0
        self.gate1=False
        self.gate2=False
        self.goal=False
        self.garage_stop=0
        self.garage_time=0.0
        self.slalom=0
        self.petbottle=0
        self.block_in_garage=0
        self.block_yukoido=0
        self.card_number_circle=0
        self.block_number_circle=0
        self.block_bingo=0
        self.entry_bonus=0
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

    def isGate1(self):
        with self.lock:
            v=self.gate1
        return v!=0

    def isGate2(self):
        with self.lock:
            v=self.gate2
        return v!=0

    def isGoal(self):
        with self.lock:
            v=self.goal
        return v!=0

    def getGarageStop(self):
        with self.lock:
            v=self.garage_stop
        return v

    def getGarageTime(self):
        with self.lock:
            v=self.garage_time
        return v

    def getSlalom(self):
        with self.lock:
            v=self.slalom
        return v

    def getPetbottle(self):
        with self.lock:
            v=self.petbottle
        return v

    def getBlockInGarage(self):
        with self.lock:
            v=self.block_in_garage
        return v

    def getBlockYukoido(self):
        with self.lock:
            v=self.block_yukoido
        return v

    def getCardNumberCircleBonus(self):
        with self.lock:
            v=self.card_number_circle
        return v

    def getBlockNumberCircleBonus(self):
        with self.lock:
            v=self.block_number_circle
        return v

    def getBlockBingo(self):
        with self.lock:
            v=self.block_bingo
        return v 

    def getEntryBonus(self):
        with self.lock:
            v=self.entry_bonus
        return v 

    def _recieveData(self, data : bytearray):
        cardNumber,blockNumber,adv_layout=unpack_from('<ii10s',data,512)
        measurement_time,run_time,gate1,gate2,goal,garage_stop,garage_time=unpack_from('<iiiiiii',data,532)
        slalom,petbottle,block_in_garage,block_yukoido,card_number_circle,block_number_circle,block_bingo,entry_bonus=unpack_from('<iiiiiiii',data,560)
        with self.lock:
            self.cardNumber=cardNumber
            self.blockNumber=blockNumber
            self.adv_layout=adv_layout
            self.measurement_time=float(measurement_time)/1000.0
            self.run_time=float(run_time)/1000.0
            self.gate1=gate1
            self.gate2=gate2
            self.goal=goal
            self.garage_stop=garage_stop
            self.garage_time=float(garage_time)/1000.0
            self.slalom=slalom
            self.petbottle=petbottle
            self.block_in_garage=block_in_garage
            self.block_yukoido=block_yukoido
            self.card_number_circle=card_number_circle
            self.block_number_circle=block_number_circle
            self.block_bingo=block_bingo
            self.entry_bonus=entry_bonus
