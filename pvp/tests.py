from unittest import TestCase
from pvp.client import run_client
from pvp.config import insert_db


class MainTestCase(TestCase):
    def test_a(self):
        #  data package must be a list, [0] - 'join', [1] - player's nick
        #self.assertTrue(run_client(['join', 'player']))
        #self.assertTrue(run_client(['join', 'obama']))
        #self.assertTrue(run_client(['join', 'putin']))
        #self.assertTrue(run_client('game'), 'incorrect data')
        #self.assertTrue(run_client(['jo', 'klava']), 'incorrect data')
        #self.assertTrue(run_client(['join', 'marusia']))
        #  match complete, wait several seconds for next match
        #self.assertTrue(run_client(['join', 'zerg']), 'wait several seconds')
        pass

    def test_b(self):
        data_true = [[1, 1, 'coca-cola', '127.0.0.1']]
        data_false = [[1, 1, '127.0.0.1']]
        self.assertTrue(insert_db(data_true), 'db insert OK')
        self.assertFalse(insert_db(data_false), 'invalid db parameters')
