from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack_into, unpack_from
import time
import threading
from hexdump import hexdump
# pip install hexdump

class ETroboSimServer:
    def __init__(self,client,embedded_address='127.0.0.1', embedded_port=54002, packet_size=1024):
        self.client=client
        self.EMBEDDED_ADDRESS=embedded_address
        self.EMBEDDED_PORT=embedded_port
        self.PACKET_SIZE=packet_size
        self.embeddedTime=0
        self.debug=False
        self.handlers = []
    
    def start(self):
        self.socket=socket(AF_INET, SOCK_DGRAM)
        self.socket.bind((self.EMBEDDED_ADDRESS, self.EMBEDDED_PORT))
        self.thread = threading.Thread(target=self.threadMethod)
        self.alive=True
        self.thread.start()

    def recievePacket(self):
        self.data, self.unity_address = self.socket.recvfrom(self.PACKET_SIZE)
        self.unityTime,=unpack_from('<Q',self.data,16)
        if(self.debug and self.unity_address[0]!=self.EMBEDDED_ADDRESS):
            print("Unity address {} is not EMBEDDED_ADDRESS {}".format(self.unity_address,self.EMBEDDED_ADDRESS))
        for handler in self.handlers:
            handler.recieveData(self.data)

    def threadMethod(self):
        i=0
        while self.alive:
            self.recievePacket()
            if(self.debug):
                #print(hexdump(self.data))
                print("Unity->Embedded: {}, UNITY_TIME: {}".format(i,self.unityTime))
            self.client.unityTime=self.unityTime        
            i=i+1

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