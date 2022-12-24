import socket
import sys
import threading
from time import sleep

sock = 0
work = True


def get_int32_from_bytes(data):
    res = int.from_bytes(data[0:4], 'big')
    data = data[4:]
    return data, res


def get_string(data):
    data, len = get_int32_from_bytes(data)
    str = data[0:len].decode('utf-8')
    data = data[len:]
    return data, str


class TcpConnection:
    def send_request_frame(self):
        frame = bytearray()
        frame.append(100)
        frame.append(0 if self.text_accepting else 1)
        self.sock.send(frame)

    def init_socket(self):
        address = sys.argv[-1]
        print(address)
        self.sock.connect((address, 8537))
        self.send_request_frame()
        print('connect')

    def close_sock(self):
        self.sock.close()

    def stop_socket(self):
        self.work = False
        self.close_sock()

    def ping_loop(self):
        while self.work:
            try:
                self.send_request_frame()
            except:
                print('disconnect')
            sleep(20)

    def start_ping_thread(self):
        thread = threading.Thread(target=self.ping_loop)
        thread.start()

    def __init__(self, text_accepting: bool, set_packet):
        self.sock = socket.socket()
        self.text_accepting = text_accepting
        self.work = True
        self.set_packet = set_packet
        thread = threading.Thread(target=self.runner)
        thread.start()
        self.start_ping_thread()

    def runner(self):
        if len(sys.argv) < 2:
            print("Enter SOG-server ip-address as command line argument")
            exit(1)

        while self.work:
            try:
                self.init_socket()
                data = b''

                while self.work:
                    packet = b''
                    packet_part = self.sock.recv(4)
                    data += packet_part
                    packet += packet_part
                    data, flag = get_int32_from_bytes(data)
                    if flag == 1:
                        packet_part = self.sock.recv(16 * 1024)
                        data += packet_part
                        packet += packet_part
                        data, text = get_string(data)
                        data, title = get_string(data)
                        self.set_packet(packet)
                    elif flag == 0:
                        packet_part = self.sock.recv(8)
                        data += packet_part
                        packet += packet_part
                        data, width = get_int32_from_bytes(data)
                        if width > 0:
                            data, height = get_int32_from_bytes(data)
                            size = height * width
                            input_size = int((size + 3) / 4)
                            while len(data) < input_size:
                                packet_part = self.sock.recv(input_size - len(data))
                                data += packet_part
                                packet += packet_part
                            self.set_packet(packet)
                            data = data[input_size:]
                        else:
                            self.set_packet(packet)
                    else:
                        print("Bad frame")
                        break
                self.close_sock()
            except:
                print("connection error")
                try:
                    self.close_sock()
                except:
                    i = 0

def close_sock():
    sock.close()


def send_chords_frame():
    global sock
    frame = bytearray()
    frame.append(100)
    frame.append(1)
    # print(frame)
    sock.send(frame)
    # print('Success')

def send_text_frame():
    global sock
    frame = bytearray()
    frame.append(100)
    frame.append(0)
    # print(frame)
    sock.send(frame)
    # print('Success')

def init_socket():
    global sock
    address = sys.argv[-1]
    print(address)
    sock = socket.socket()
    sock.connect((address, 8537))
    # print(sock)
    # send_chords_frame()
    send_text_frame()
    print('connect')
    
    
def get_text(set_text, set_packet):
    if len(sys.argv) < 2:
        print("Enter SOG-server ip-address as command line argument")
        exit(1)

    while work:
        try:
        # if True:
            global sock
            init_socket()
            data = b''

            while work:
                packet = b''
                packetPart = sock.recv(4)
                data += packetPart
                packet += packetPart
                # print('\n\n\n', data)
                data, flag = get_int32_from_bytes(data)
                # print(flag)
                if (flag == 1):
                    packetPart = sock.recv(16 * 1024)
                    print(packetPart)
                    data += packetPart
                    packet += packetPart
                    data, text = get_string(data)
                    data, title = get_string(data)
                    set_text(text, title, packet)
                elif (flag == 0): 
                    packetPart = sock.recv(8)
                    data += packetPart
                    packet += packetPart
                    data, width = get_int32_from_bytes(data)
                    # print(width)
                    if (width > 0):
                        data, height = get_int32_from_bytes(data)
                        size = height * width
                        inputSize = int((size + 3) / 4)
                        while len(data) < inputSize:
                            # print(len(data))
                            packetPart = sock.recv(inputSize - len(data))
                            data += packetPart
                            packet += packetPart
                            # print(len(data), inputSize)
                        # print(data, width, height, inputSize)
                        set_packet(packet)
                        data = data[inputSize:]
                    else:
                        set_packet(packet)
                else:
                    print("Bad frame")
                    break
            close_sock()
        except:        
            print("connection error")
            try:
                close_sock()
            except:
                i = 0

def ping_loop():
    while work:
        try:
            send_chords_frame()
        except:
            print('disconnect')
        sleep(20)
        

def start_ping_thread():
    thread = threading.Thread(target=ping_loop)
    thread.start()


def start_socket(par):
    thread = threading.Thread(target=get_text, args=(par.setup_text, par.setup_packet))
    thread.start()
    start_ping_thread()


def stop_socket():
    global work
    work = False
    close_sock()
