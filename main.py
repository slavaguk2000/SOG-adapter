import math
import sys  # sys нужен для передачи argv в QApplication
from tcp import start_socket, stop_socket, TcpConnection
from socket import socket
import threading


class AdapterCore:
    chord_sockets = []
    text_sockets = []
    server_socket = 0
    work = True

    def set_text_packet(self, packet):
        self.text_packet = packet
        invalid_sockets = []
        for sock in self.text_sockets:
            try:
                sock.send(packet)
            except:
                invalid_sockets.append(sock)
        for invSock in invalid_sockets:
            try:
                self.text_sockets.remove(invSock)
                invSock.close()
            except:
                pass

    def set_chords_packet(self, packet):
        self.chord_packet = packet
        invalid_sockets = []
        for sock in self.chord_sockets:
            try:
                sock.send(packet)
            except:
                invalid_sockets.append(sock)
        for invSock in invalid_sockets:
            try:
                self.chord_sockets.remove(invSock)
                invSock.close()
            except:
                pass

    def __init__(self):
        self.chord_packet = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        self.text_packet = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        TcpConnection(True, self.set_text_packet)
        TcpConnection(False, self.set_chords_packet)
        thread = threading.Thread(target=self.start_accepting)
        thread.start()

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
                    if (len(self.chord_packet)):
                        try:
                            s.send(self.chord_packet)
                            self.chord_sockets.append(s)
                        except:
                            pass
                if firstPacket == b'd\x00':
                    if len(self.text_packet):
                        try:
                            s.send(self.text_packet)
                            self.chord_sockets.append(s)
                        except:
                            pass
            except:
                pass

    def end(self):
        self.work = False
        if self.server_socket:
            self.server_socket.close()


def main():
    exit = 'a'
    adapter = AdapterCore()
    while exit != 'e':
        exit = input()
    adapter.end()

main()