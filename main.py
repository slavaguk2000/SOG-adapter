import math
import sys  # sys нужен для передачи argv в QApplication
from tcp import start_socket, stop_socket
from socket import socket
import threading

class AdapterCore(): 
    packet = b'\x00\x00\x00\x00\x00\x00\x00\x00'
    chord_sockets = []
    text_sockets = []
    server_socket = 0
    work = True

    def __init__(self):
        self.packet = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        self.textPacket = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        start_socket(self)
        thread = threading.Thread(target=self.start_accepting)
        thread.start()

    def setup_text(self, text, title, text_packet):
        print(text, title)
        # self.textPacket = text_packet
        # invalid_sockects = []
        # for sock in self.text_sockets:
        #     try:
        #         sock.send(text_packet)
        #     except:
        #         invalid_sockects.append(sock)
        # for invSock in invalid_sockects:
        #     try:
        #         self.text_sockets.remove(invSock)
        #         invSock.close()
        #     except:
        #         pass
        # print(len(self.text_sockets))

    def setup_packet(self, packet):
        self.packet = packet
        # print(packet)
        invalid_sockects = []
        for sock in self.chord_sockets:
            try:
                sock.send(packet)
            except:
                invalid_sockects.append(sock)
        for invSock in invalid_sockects:
            try:
                self.chord_sockets.remove(invSock)
                invSock.close()
            except:
                pass
        print(len(self.chord_sockets))

    def start_accepting(self):
        self.server_socket = socket()
        self.server_socket.bind(('', 8536))
        self.server_socket.listen(10)
        while self.work:
            try:
                s, addr = self.server_socket.accept()
                print('Connect: ',addr)
                firstPacket = s.recv(2)
                if firstPacket == b'd\x01':
                    if (len(self.packet)):
                        try:
                            s.send(self.packet)
                            self.chprdsSockets.append(s)
                        except:
                            pass
                if firstPacket == b'd\x00':
                    if (len(self.textPacket)):
                        try:
                            s.send(self.textPacket)
                            self.chprdsSockets.append(s)
                        except:
                            pass
            except:
                pass

    def end(self):
        self.work = False
        if (self.server_socket):
            self.server_socket.close()


def main():
    exit = 'a'
    adapter = AdapterCore()
    while(exit != 'e'):
        exit = input()
    adapter.end()

main()