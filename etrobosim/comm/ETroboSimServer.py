from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack_into, unpack_from
import time
import threading
import asyncio


class ETroboSimServer():

    def __init__(self,client,embedded_address='127.0.0.1', embedded_port=54002, packet_size=1024,handlers=[]):
        self.embeddedTime=0
        self.debug=False
        self.handlers =handlers
        self.alive=False
        self.client=client
        self.EMBEDDED_ADDRESS=embedded_address
        self.EMBEDDED_PORT=embedded_port
        self.PACKET_SIZE=packet_size
        self.thread = None
    
    def start(self):
        self.socket=socket(AF_INET, SOCK_DGRAM)
        self.thread = threading.Thread(target=self.threadMethod)
        self.alive=True
        self.thread.start()

    def threadMethod(self):
        asyncio.run(self.server())

    async def server(self):
        print("Starting UDP server")
        loop = asyncio.get_running_loop()
        transport, protocol = await loop.create_datagram_endpoint(
            lambda: ETroboSimServer(self.client,self.EMBEDDED_ADDRESS, self.EMBEDDED_PORT, self.PACKET_SIZE,self.handlers), 
            local_addr=(self.EMBEDDED_ADDRESS, self.EMBEDDED_PORT))
        try:
            while(self.alive):
                await asyncio.sleep(1) 
        finally:
            transport.close()

    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        self.data=data
        self.unity_address=addr
        self.unityTime,=unpack_from('<Q',self.data,16) 
        self.client.unityTime=self.unityTime 
        # print("datagram_received: Unity Time {} ".format(self.unityTime))
        if(self.debug and self.unity_address[0]!=self.EMBEDDED_ADDRESS):
            print("Unity address {} is not EMBEDDED_ADDRESS {}".format(self.unity_address,self.EMBEDDED_ADDRESS))
        for handler in self.handlers:
            handler._recieveData(self.data)
    
    def connection_lost(self, exc):
        # print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

    def addHandler(self, handler):
        self.handlers.append(handler)
        return self
    
    def removeHandler(self, handler):
        self.handlers.remove(handler)
        return self

    def exit_process(self):
        self.alive=False
        if self.thread is not None:
            self.thread.join()
    
    def __del__(self):
        self.exit_process()

