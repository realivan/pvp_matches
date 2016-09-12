#!/usr/bin/python
# coding: utf8

import asyncio
from pvp.config import insert_db
from pvp import Common, ProcessData


class Server(asyncio.Protocol):
    def __init__(self):
        self.match_wait_time = 3  # секунд

    def connection_made(self, transport):
        self.transport = transport
        asyncio.ensure_future(self.made_match())

    def data_received(self, data):
        data = ProcessData.read(data)
        if data and data[0] == 'join' and type(data[1]) == str:
            self.nick = data[1]
            self.peername = self.transport.get_extra_info('peername')
            print('Connection from {}'.format(self.peername))
            if not Common['go']:
                asyncio.ensure_future(self.new_player())
        else:
            ProcessData.send('incorrect data', self.transport)
            print('incorrect data')
            self.transport.close()

    @asyncio.coroutine
    def new_player(self):
        if Common['clients_numbers'] != 0:  # если клиент попадает в матч, то сразу получает информацию о матче
            Common['clients_numbers'] -= 1
            Common['clients'].append(self.transport)
            Common['game'].append([Common['match_id'], len(Common['game']), self.nick, self.peername[0]])  # [id match, id player, nick, ip]
            # при подключении нового игрока делаем рассылку всем игрокам
            for key in Common['clients']:
                ProcessData.send(Common['game'], key)
            if Common['clients_numbers'] == 0:
                Common['go'] = True
                insert_db(Common['game'])
                yield from asyncio.sleep(0.1)
                for key in Common['clients']:
                    ProcessData.send('create match', key)

    @asyncio.coroutine
    def made_match(self):
        if Common['clients_numbers'] == 0:
            # если не попадает, то ждет match_wait_time следующего матча
            while self.match_wait_time != 0:
                yield from asyncio.sleep(1)  # ждем секунду
                self.match_wait_time -= 1
                if self.match_wait_time == 0:
                    ProcessData.send('no any matches', self.transport)
                    print('Time is out, the server closed the connection for {}'.format(self.peername))
                    self.transport.close()
                elif not Common['go']:  # есть возможность создать новый матч, подключаем игрока
                    asyncio.ensure_future(self.new_player())
                    break
                else:
                    ProcessData.send('wait please', self.transport)

    def connection_lost(self, exc):
        print('The server closed the connection for {}'.format(self.peername))
        self.transport.close()
