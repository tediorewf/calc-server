#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import socket
import re

from twisted.internet import reactor, protocol, endpoints


VARIABLE_NAME_PATTERN = r'^[a-zA-Z_][a-zA-Z_0-9]*$'
variable_name_regexp = re.compile(VARIABLE_NAME_PATTERN)


class ProcessClient(protocol.Protocol):
    DATA_ENCODING = 'utf-8'
    QUERIES_DELIMITER = '\r\n'

    def __init__(self, server):
        self.server = server
        self.dataForProcessing = ''

    def connectionMade(self):
        self.server.concurrentClientCount += 1
        print('{} concurrent clients are connected'.format(
            self.server.concurrentClientCount))

    def connectionLost(self, reason):
        self.server.concurrentClientCount -= 1

    def dataReceived(self, data):
        #self - это клиент
        decoded_data = data.decode(self.DATA_ENCODING)
        print('Data received: {}'.format(decoded_data))
        queries = self.dataForProcessing + decoded_data
        queries = queries.split(self.QUERIES_DELIMITER)
        self.dataForProcessing = queries[-1]
        del queries[-1]
        for query in queries:
            self.__processQuery(query)

    def __processQuery(self, query):
        words = query.split()

        if len(words) != 4:
            self.__writeErr()
            return

        self.__writeAnswer(
            operation=words[1], operand1=words[2], operand2=words[3]
        )

    def __writeAnswer(self, operation, operand1, operand2):
        answer = self.__getAnswer(operation, operand1, operand2)

        if answer is None:
            self.__writeErr()
            print('An error occurred')
            return

        self.__write('OK {}'.format(answer))
        print('Answer: {}'.format(answer))

    def __getAnswer(self, operation, operand1, operand2):
        parsed_operand1 = self.__parseOperand(operand1)
        parsed_operand2 = self.__parseOperand(operand2)

        if parsed_operand1 is None and parsed_operand2 is None:
            return None

        answer = None

        if operation == '+':
            answer = parsed_operand1 + parsed_operand2
        elif operation == '*':
            answer = parsed_operand1 * parsed_operand2
        elif operation == '-':
            answer = parsed_operand1 - parsed_operand2
        elif operation == '/':
            try:
                answer = parsed_operand1 / parsed_operand2
            except ZeroDivisionError:
                answer = float('infinity')
        elif operation == '=':
            if self.__isVariableName(operand1):
                answer = self.server.sharedVariables[operand1] = parsed_operand2

        return answer

    def __writeErr(self):
        self.__write('ERR')

    def __write(self, response: str):
        self.transport.write(
            (response + self.QUERIES_DELIMITER).encode(self.DATA_ENCODING)
        )

    def __parseOperand(self, operand: str) -> int or None:
        if self.__isVariableName(operand):
            parsed = self.server.sharedVariables.get(operand) or None
        else:
            try:
                parsed = float(operand)
            except ValueError:
                parsed = None

        return parsed

    def __isVariableName(self, candidate) -> bool:
        return bool(variable_name_regexp.match(candidate))


class Server(protocol.Factory):
    def __init__(self):
        self.concurrentClientCount = 0
        self.sharedVariables = {}

    def buildProtocol(self, addr):
        return ProcessClient(self)


def print_host_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    print(
        'Host name: {}\nIP address: {}'.format(hostname, ip_address)
    )


def run_server():
    print('Starting TCP-based CALC server. Ctrl-C to stop')
    endpoints.serverFromString(reactor, 'tcp:28563').listen(Server())
    reactor.run()
    print('The server has stopped')


if __name__ == '__main__':
    print_host_info()
    run_server()
