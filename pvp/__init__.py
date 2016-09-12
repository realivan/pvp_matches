import pickle
import asyncio
from pvp.config import insert_match
from threading import Thread


class ProcessData:
    @staticmethod
    def send(data, transport):
        try:
            print('-> {!r}'.format(data))
            data = pickle.dumps([len(data), data])
            transport.write(data)
        except:
            pass

    @staticmethod
    def read(data):
        try:
            data = pickle.loads(data)
            data = data[1][:data[0]]
            print('<- ', data)
        except:
            return None
        return data


@asyncio.coroutine
def start_new_match():
    try:
        while True:
            yield from asyncio.sleep(1)
            if Common['clients_numbers'] == 0:
                yield from asyncio.sleep(Common['next_match'])  # ждем next_match секунд чтобы начать набор на новый матч
                for key in Common['clients']:  # отключаем игроков для которых уже создался матч
                    key.close()
                Common['game'] = []
                Common['go'] = False
                Common['clients_numbers'] = 4
                Common['match_id'] += 1
                Common['clients'] = []
                insert_match(Common['clients_numbers'])  # записываем данные о новом матче в бд
    except:
        pass

__version__ = '1.0'
Common = {
    'game': [],
    'go': False,
    'clients_numbers': 4,
    'match_id': 1,
    'clients': [],
    'next_match': 5,
    'error': False
}
