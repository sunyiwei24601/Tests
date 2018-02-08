from socket import *
from time import ctime

HOST=''
PORT=21567
BUFSIZ=1024
ADDR=(HOST,PORT)
print(233)
tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print("waiting for connection...")
    tcpCliSock,addr=tcpSerSock.accept()
    print("...connected from",addr)

    while True:
        data=tcpCliSock.recv(BUFSIZ)
        if not data:
            break
        tcpCliSock.send(("[{}]{}".format(ctime(),data)).encode("utf-8"))

tcpCliSock.close()
tcpSerSock.close()
