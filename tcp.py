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
    sock.connect((address, 8536))
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
                    # print(text)
                    data, title = get_string(data)
                    # print(title)
                    # print(set_text)
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
