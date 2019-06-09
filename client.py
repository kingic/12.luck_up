import socket
import socketserver 
from os.path import exists
HOST = ''
PORT = ''
 
def getFileFromServer(filename):
    data_transferred = 0
 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT)) 
        print('file[%s] starting transmission...' %filename)
        filename = filename.encode()
        with open(filename, 'rb') as f:
            try:
                data = f.read(1024) 
                while data: 
                    data_transferred += sock.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)
 
    print('file[%s] finish transmission. transmission amount [%d]' %(filename, data_transferred))
 
filename = input('enter file name that you download:')
getFileFromServer(filename)
