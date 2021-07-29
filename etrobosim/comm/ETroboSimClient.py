from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack_into, unpack_from
import time
import threading

class ETroboSimClient():
    def __init__(self, interval=0.01, unity_address='127.0.0.1', unity_port=54001, packet_size=1024,timeout=1):
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
        self.debug=False
        self.handlers = []
        self.timeout = timeout

    def start(self):
        self.socket=socket(AF_INET, SOCK_DGRAM)
        self.thread = threading.Thread(target=self.threadMethod)
        self.alive=True
        self.thread.start()

    def sendPacket(self):
        pack_into('<QQ',self.data,8,self.embeddedTime,self.unityTime)
        pack_into('<I' ,self.data,32,self.led)
        for handler in self.handlers:
            handler._sendData(self.data)
        self.socket.sendto(self.data, (self.UNITY_ADDRESS, self.UNITY_PORT))

    def threadMethod(self):
        i=0
        starttime=time.time()
        while self.alive:
            if self.debug:
                print("unitytime={},embeddedTime={}".format(self.unityTime,self.embeddedTime))
            if(self.embeddedTime<=self.unityTime):
                self.sendPacket()
                self.embeddedTime=self.embeddedTime+(int)(self.interval*1000000)
                starttime=time.time()
                i=i+1
            else:
                if(self.timeout>0 and time.time()-starttime>self.timeout):
                    self.alive=False
                else:
                    time.sleep(0.001)


    def addHandler(self, handler):
        self.handlers.append(handler)
        return self
    
    def removeHandler(self, handler):
        self.handlers.remove(handler)
        return self

    def exit_process(self):
        self.alive=False
        self.thread.join()

    def __del__(self):
        self.exit_process()

