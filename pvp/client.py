#!/usr/bin/python
# coding: utf8

import asyncio
from pvp import Common, ProcessData


class Client(asyncio.Protocol):
    def __init__(self, message, loop):
        self.loop = loop
        self.message = message

    def connection_made(self, transport):
        self.transport = transport
        ProcessData.send(self.message, self.transport)

    def data_received(self, data):
        if ProcessData.read(data) == 'incorrect data':
            Common['error'] = True

    def connection_lost(self, exc):
        print('The server closed the connection')
        self.loop.stop()


def run_client(mes):
    loop = asyncio.get_event_loop()
    coro = loop.create_connection(lambda: Client(mes, loop), '127.0.0.1', 4004)
    loop.run_until_complete(coro)
    loop.run_forever()
    loop.close()
    if Common['error']:
        return False
    return True

if __name__ == '__main__':
    message = ['join', 'player']
    run_client(message)
