import socket
import argparse
import sys

parser = argparse.ArgumentParser(usage = '\n--Host (-H) [TARGET-HOST ex. -H 192.168.0.1]\n--Port (-p) [TARGET-PORT (ex. 21)]\n--Type (-t) [TYPE-OF-CONN.]')
parser.add_argument("-H", "--host", help = 'Give Target Host! (192.168.0.1)', required = True)
parser.add_argument("-p", "--port", nargs = 1, help = 'Give Target Port! (80)', required = True)
parser.add_argument("-t", "--type", nargs = 1, help = 'Type Of Connection (UDP/TCP, u/t)!', required = True)
netargs = parser.parse_args()
target_host = netargs.host
target_port = int(netargs.port[0])
target_type = str(netargs.type[0])

def connect(host, port, type):
    if (type == 't'):
        current_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    elif (str(type) == 'u'):
        current_connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        print("Type Not Recognized!")
        print(type)
        sys.exit(1)
    for x in range(3):
        if (type == 't'):
            try:
                current_connection.connect((host, port))
                print('TCP Connection initialized to '+host)
            except socket.error:
                print("Error connection to remote host")
            try:
                current_connection.send("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n")
                print("Data Successfully Sent via TCP")
            except socket.error:
                print("Error sending data on socket")
            try:
                current_response = current_connection.recv(4096)
                print("Data Received from Remote Host")
                print(current_response)
            except socket.error:
                print("Error Receiving Response from "+host)
        elif (type == 'u'):
            data = "TEST"
            data = data.encode(encoding = 'utf-8')
            try:
                current_connection.sendto(bytes(data), (host, port))
                print("Data Sucessfully sent via UDP")
            except socket.error:
                print("Error Sending data via UDP")
            try:
                current_response = current_connection.recvfrom(4096)
                print("UDP Response Received")
                print(current_response)
            except socket.error:
                print("Error Receiving Response from "+host)

def main():
    connect(target_host, target_port, target_type)

main()
