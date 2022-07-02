import math
import sys  # sys нужен для передачи argv в QApplication
from tcp import start_socket, stop_socket
from socket import socket
import threading

class AdapterCore(): 
    packet = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    sockets = []
    serverSocket = 0
    work = True

    def __init__(self):
        self.packet = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        start_socket(self)
        thread = threading.Thread(target=self.start_accepting)
        thread.start()

    def setup_text(self, text, title):
        print(text, title)

    def setup_packet(self, packet):
        self.packet = packet
        # print(packet)
        invalidSockects = []
        for sock in self.sockets:
            try:
                sock.send(packet)
            except:
                invalidSockects.append(sock)   
        for invSock in invalidSockects:
            try:
                self.sockets.remove(invSock)
                invSock.close()
            except:
                pass
        print(len(self.sockets))

    def start_accepting(self):
        self.serverSocket = socket()
        self.serverSocket.bind(('', 8536))
        self.serverSocket.listen(10)
        while self.work:
            try:
                s, addr = self.serverSocket.accept()
                print('Connect: ',addr)
                firstPacket = s.recv(2)
                if firstPacket == b'd\x01':
                    if (len(self.packet)):
                        try:
                            s.send(self.packet)
                            self.sockets.append(s)
                        except:
                            pass
            except:
                pass

    def end(self):
        self.work = False
        if (self.serverSocket):
            self.serverSocket.close()


def main():
    exit = 'a'
    adapter = AdapterCore()
    while(exit != 'e'):
        exit = input()
    adapter.end()

main()