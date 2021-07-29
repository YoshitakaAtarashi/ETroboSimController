from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack_into, unpack_from
import time
import threading
from .comm import ETroboSimClient, ETroboSimServer
from enum import Enum

class Course(Enum):
    LEFT = 0
    RIGHT = 1

class Controller:
    def __init__(self, course:Course = Course.LEFT):
        if course==Course.LEFT:
            self.client=ETroboSimClient()
            self.server=ETroboSimServer(self.client)
        else:
            self.client=ETroboSimClient(unity_port=54003)
            self.server=ETroboSimServer(self.client,embedded_port=54004)

    def start(self,debug=False):
        self.client.debug=debug
        self.client.start()
        self.server.debug=debug
        self.server.start()
        self.debug=debug
    
    def exit_process(self):
        if self.debug:
            print("exit_process(): client")
        self.client.exit_process()
        if self.debug:
            print("exit_process(): server")
        self.server.exit_process()
        if self.debug:
            print("exit_process(): end")

    def isAlive(self):
        return self.server.alive and self.client.alive

    def addHandler(self, handler):
        if hasattr(handler,'_sendData'):
            self.client.addHandler(handler)
        if hasattr(handler,'_recieveData'):
            self.server.addHandler(handler)

    def addHandlers(self, handlers):
        for handler in handlers:
            self.addHandler(handler)

    def runCyclic(self, function, interval=0.01):
        self.client.interval=interval
        target_time=self.client.embeddedTime
        while self.isAlive():
            if target_time<=self.client.embeddedTime:                
                function()
                target_time=target_time+interval*1000000
            else:
                # 少し待つ。
                time.sleep(0.001)




