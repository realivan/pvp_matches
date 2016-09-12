#!/usr/bin/python
# coding: utf8

import asyncio
from pvp.server import Server
from pvp import start_new_match


def main():
    loop = asyncio.get_event_loop()
    # Each client connection will create a new instance
    coro = loop.create_server(Server, '', 4004)
    server = loop.run_until_complete(coro)
    # функция определяет создание матча и через next_match время сбрасывает значения для следующего матча
    asyncio.ensure_future(start_new_match())

    # Serve requests until Ctrl+C is pressed
    print('Server started {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

if __name__ == '__main__':
    main()
