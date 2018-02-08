from twisted.internet import protocol,reactor

HOST='localhost'
PORT=21567

class TSClntProtocol(protocol.Protocol):
    def sendData(self):
        data=input('>')
        if data:
            print('...sending data%s...'%data)
            self.transport.write(data.encode('utf-8'))
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        print(data)
        self.sendData()
class TSClntFactory(protocol.ClientFactory):
    protocol=TSClntProtocol
    clientConnectionLost=clientConnectionFailed=lambda self,connector,reason:reactor.stop()

reactor.connectTCP(HOST,PORT,TSClntFactory())
reactor.run()
