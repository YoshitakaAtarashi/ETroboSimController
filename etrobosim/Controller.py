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
        self.client.exit_process()
        self.server.exit_process()

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
        base_time=self.client.unityTime
        target_time=base_time+1
        while self.isAlive():
            function()
            time.sleep(interval)
        print("runCyclic: end")



