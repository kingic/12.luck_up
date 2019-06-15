import socketserver
import socket
from os.path import exists
 
HOST = '172.31.44.149'
PORT = 3000
i = 0

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0
        print('[%s] connected' %self.client_address[0])

        data = self.request.recv(1024) 
        if not data:
            print('file[%s]: does not exist server, or transfer error' %date)
            return

        j = str(i)
        i = i+1
        with open('download/' + "test"+j+ ".jpg", 'wb') as f:
            try:
                while  data:
                    f.write(data)
                    data_transferred += len(data)
                    data = self.request.recv(1024)
            except Exception as e:
                print(e)

        conn, addr = server.accept()
        with conn:
            print('Connected by', addr)
        print('complete transmission[%s], transmission amount[%d]' %(data,data_transferred))
 
def runServer():
    print('++++++file server start++++++')
    print("+++if you want to finish file server, press'Ctrl + C'")
 
    try:
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('++++++end file server++++++')
 
 
runServer()
