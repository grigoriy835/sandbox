import os
os.environ['RUN_MOD'] = 'TEST'

from handlers import *
from aiohttp.test_utils import make_mocked_request
import unittest


class FakeRequestCase(unittest.TestCase):
    def test_app(self):
        pass
