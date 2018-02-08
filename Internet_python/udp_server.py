import socketserver
from socket import *
from time import ctime
HOST=""
PORT=21567
BUFSIZ=1024
ADDR=(HOST,PORT)

udpSerSock=socket(AF_INET,SOCK_DGRAM)
udpSerSock.bind(ADDR)
print(udpSerSock.getsockname())
while True:
    print("waiting for message:")
    data,addr=udpSerSock.recvfrom(BUFSIZ)
    udpSerSock.sendto(('[%s]%s'%(ctime(),data)).encode("utf-8"),addr)
    print('...recevied from and returned to:',addr)

udpSerSock.close()