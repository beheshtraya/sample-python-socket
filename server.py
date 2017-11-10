import datetime
"""
Socket Programming with multi-threading (server)
beheshtraya@gmail.com
"""


import threading
import socket
from os import system

HOST = "127.0.0.1"
TIME_PORT = 6666
CALC_PORT = 7777
COMMAND_PORT = 8888

print ("---- Socket Programming with multi-threading (server) ----")

def time_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, TIME_PORT))
    server.listen(5)

    while True:
        client_socket, (client_address, client_port) = server.accept()
        print ('Time request from', str(client_address), str(client_port))
        t = str(datetime.datetime.now()).encode()
        client_socket.sendall(t)



def calc_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, CALC_PORT))
    server.listen(5)

    while True:
        client_socket, (client_address, client_port) = server.accept()
        print ('Calculation request from', str(client_address), str(client_port))
        i = client_socket.recv(1024).decode().strip()
        try:
            if i.__contains__('+'):
                op_index = i.find('+')
                var1 = int(i[:op_index].strip())
                var2 = int(i[op_index+1:].strip())
                o = str(var1 + var2).encode()
                client_socket.send(o)
            elif i.__contains__('-'):
                op_index = i.find('-')
                var1 = int(i[:op_index].strip())
                var2 = int(i[op_index+1:].strip())
                o = str(var1 - var2).encode()
                client_socket.send(o)
            elif i.__contains__('*'):
                op_index = i.find('*')
                var1 = int(i[:op_index].strip())
                var2 = int(i[op_index+1:].strip())
                o = str(var1 * var2).encode()
                client_socket.send(o)
            elif i.__contains__('/'):
                op_index = i.find('/')
                var1 = int(i[:op_index].strip())
                var2 = int(i[op_index+1:].strip())
                if var2 == 0:
                    o = 'Error: Division by Zero'.encode()
                    client_socket.send(o)
                else:
                    o = str(var1 / var2).encode()
                    client_socket.send(o)
                
            else:
                client_socket.send('Unknown operation')
        except:
            client_socket.send('Unknown operation')


def command_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, COMMAND_PORT))
    server.listen(5)

    while True:
        client_socket, (client_address, client_port) = server.accept()
        print ('System command request from', str(client_address), str(client_port))
        command = client_socket.recv(1024).decode().strip()
        status = system(command)
        o = str('Exit status:' + str(status)).encode()
        client_socket.send(o)
        
        
time_server_thread = threading.Thread(target=time_server)
time_server_thread.start()

calc_server_thread = threading.Thread(target=calc_server)
calc_server_thread.start()

command_server_thread = threading.Thread(target=command_server)
command_server_thread.start()



