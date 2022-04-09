#!/usr/bin/python
# -*- coding: UTF-8 -*-

from twisted.internet import reactor, protocol, endpoints

class ProcessClient(protocol.Protocol):
    def __init__(self, server):
        self.server = server
        self.dataForProcessing = ""

    def connectionMade(self):
        self.server.concurrentClientCount += 1
        print(str(self.server.concurrentClientCount) + " concurrent clients are connected")

    def connectionLost(self, reason):
        self.server.concurrentClientCount -= 1

    def dataReceived(self, data):
        #self - это клиент
        data = data.decode('utf8')
        print("Data received: "+data)
        queries = self.dataForProcessing + data;
        queries = queries.split("\r\n");
        self.dataForProcessing = queries[-1];
        del queries[-1]
        for query in queries:
            words = query.split(" ")
            answer = str(eval(words[2]+words[1]+words[3]))
            self.transport.write((answer+"\r\n").encode('utf8'))
            print("Answer: "+answer)

class Server(protocol.Factory):
    def __init__(self):
        self.concurrentClientCount = 0

    def buildProtocol(self, addr):
        return ProcessClient(self)

endpoints.serverFromString(reactor, "tcp:28563").listen(Server())
reactor.run()
