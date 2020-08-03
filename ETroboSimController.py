from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack_into, unpack_from
import time
import threading
from hexdump import hexdump
# pip install hexdump
from comm.ETroboSimClient import ETroboSimClient
from comm.ETroboSimServer import ETroboSimServer

class ETroboSimController:
    def __init__(self):
        self.client=ETroboSimClient()
        self.server=ETroboSimServer(self.client)

    def start(self,debug=False):
        self.server.debug=debug
        self.client.debug=debug
        try:
            while self.server.alive and self.client.alive:
                if(debug):
                    print(self.server)
                    print(self.client)
                time.sleep(1)

        except KeyboardInterrupt:
            self.exit_process()
            raise
    
    def exit_process(self):
        self.client.exit_process()
        self.server.exit_process()


controller=ETroboSimController()
controller.start(debug=True)
controller.exit_process()


