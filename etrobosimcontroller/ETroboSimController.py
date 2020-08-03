from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack_into, unpack_from
import time
import threading
from .comm import ETroboSimClient, ETroboSimServer

class ETroboSimController:
    def __init__(self, isL:bool = True):
        self.lsL=isL
        self.client=ETroboSimClient()
        self.server=ETroboSimServer(self.client)

    def start(self,debug=False):
        #isLでポートを変えたい。
        self.client.debug=debug
        self.client.start()
        self.server.debug=debug
        self.server.start()
    
    def exit_process(self):
        self.client.exit_process()
        self.server.exit_process()

    def isAlive(self):
        return self.server.alive and self.client.alive

    def add(self, handler):
        if hasattr(handler,'updateData'):
            self.client.addHandler(handler)
        if hasattr(handler,'recieveData'):
            self.server.addHandler(handler)



