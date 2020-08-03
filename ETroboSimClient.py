from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack_into, unpack_from
import time
import threading

class ETroboSimClient:
    def __init__(self, interval=0.01, unity_address='127.0.0.1', unity_port=54001, packet_size=1024):
        self.UNITY_ADDRESS=unity_address
        self.UNITY_PORT=unity_port
        self.PACKET_SIZE=packet_size
        self.interval=interval
        self.data= bytearray(self.PACKET_SIZE)
        pack_into('<4sI',self.data,0,b'ETTX',1)
        pack_into('<II' ,self.data,24,512,512)
        self.embeddedTime=0
        self.unityTime=0
        self.led=3
        self.socket=socket(AF_INET, SOCK_DGRAM)
        self.thread = threading.Thread(target=self.threadMethod)
        self.alive=True
        self.thread.start()
        self.debug=False

    def updateData(self):
        pack_into('<QQ',self.data,8,self.embeddedTime,self.unityTime)
        pack_into('<I' ,self.data,32,self.led)
        pack_into('<IIII' ,self.data,36,0,50,50,0) # motor

    def sendPacket(self):
        self.socket.sendto(self.data, (self.UNITY_ADDRESS, self.UNITY_PORT))

    def threadMethod(self):
        i=0
        base_time = time.time()
        target_time=self.interval
        while self.alive:
            self.updateData()        
            self.sendPacket()
            t=time.time()
            sleeptime = target_time-(t-base_time)
            self.embeddedTime=self.embeddedTime+(int)(self.interval*1000000)
            target_time+=self.interval
            if(self.debug):
                print("Embedded->Unity: {}, EMBEDDED_TIME: {}, REAL_TIME: {}, SLEEP:{}".format(i,self.embeddedTime,t-base_time,sleeptime))
            if sleeptime>0:
                time.sleep(sleeptime)
            i=i+1

    def exit_process(self):
        self.alive=False
        self.thread.join()

    def __del__(self):
        self.exit_process()

