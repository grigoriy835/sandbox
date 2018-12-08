import os
os.environ['RUN_MOD'] = 'TEST'

import unittest
import json
from handlers import *
from aiohttp.test_utils import make_mocked_request
from unittest import mock
from helpers import DbHelper
from dbModels import *
import time
import asyncio


class TestComponentsCase(unittest.TestCase):
    def test_parser(self):  # 1123 stream

        # невалидные прогоны

        self.cleanBases()
        # левый хэш
        req = make_mocked_request('GET', '/', headers={'User-Agent': ''})
        parser = RequestParser(req, shash='111')
        assert not parser.isValid()
        assert parser.tbReason is None

        # нет юзерагента
        req = make_mocked_request('GET', '/', headers={})
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason is None

        # нет ip(peername)
        ua = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-T116 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 YaBrowser/15.2.2214.3725.01 Safari/537.36'
        req = make_mocked_request('GET', '/', headers={'User-Agent': ua})
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason is None

        # по ip нет подходящего оператора
        req = make_mocked_request('GET', '/', headers={'User-Agent': ua}, transport=self.getTransport('0.0.0.0'))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason == 2

        # не нашли сплит
        req = make_mocked_request('GET', '/',
                                  headers={
                                      'User-Agent': ua,
                                      'HTTP_REFERER': 'https://vk.com/mikhailkharchev',
                                      'COOKIE': 'fc0bbd68687f68b791690200c02a9534_d2b6043e84b2aebc95a2faf382bde230=99'
                                  },
                                  transport=self.getTransport('78.25.121.52'))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason == 8

        # пустой юзерагент
        ua = ''
        req = make_mocked_request('GET', '/', headers={'User-Agent': ua}, transport=self.getTransport('78.25.121.52'))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason == 10

        # прогон с левым юзерагентом, не должен определится тип устройства parser.type
        ua = 'Huyopera/9.80 (Huyroid; Huyopera Huini/7.6.40234/36.2592; U; ru) Huyesto/2.12.423 Version/12.16'
        req = make_mocked_request('GET', '/', headers={'User-Agent': ua}, transport=self.getTransport('78.25.121.52'))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason == 10

        # в реферере стоп слово
        ua = 'Opera/9.80 (Android; Opera Mini/7.6.40234/36.2592; U; ru) Presto/2.12.423 Version/12.16'
        req = make_mocked_request('GET', '/', headers={'User-Agent': ua, 'HTTP_REFERER': 'https://vklolicon.com/mikhailkharchev',}, transport=self.getTransport('78.25.121.52'))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason == 13

        # плохой реферер
        req = make_mocked_request('GET', '/', headers={'User-Agent': ua, 'HTTP_REFERER': 'https://freehundsex.com/so_bad_ref',}, transport=self.getTransport('78.25.121.52'))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        assert not parser.isValid()
        assert parser.tbReason == 13

#  валидные прогоны

        self.cleanBases()

        # базовый прогон на пустую базу/редис
        ua = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-T116 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 YaBrowser/15.2.2214.3725.01 Safari/537.36'
        req = make_mocked_request('GET', '/?landing=311', headers={'User-Agent': ua}, transport=self.getTransport('78.25.121.52'))
        start = int(round(time.time() * 1000))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        time1 = int(round(time.time() * 1000)) - start
        assert parser.isValid()

        # такой же прогон, всё из редиса
        req = make_mocked_request('GET', '/?', headers={'User-Agent': ua}, transport=self.getTransport('78.25.121.52'))
        start = int(round(time.time() * 1000))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        time2 = int(round(time.time() * 1000)) - start
        assert parser.isValid()

        # тоже самое но фром скрипт
        req = make_mocked_request('GET', '/')
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534', fromScript=True,
                               data={
                                   'HTTP_USER_AGENT': ua,
                                   'HTTP_X_FORWARDED_FOR': '77.244.121.69, sdfsafsa',
                                   'HTTP_REFERER': 'https://vk.com/mikhailkharchev',
                               })  # 1123 stream
        assert parser.isValid()

        # прогон на непустую базу, которая будет дополнена новыми данными
        ua = 'Opera/9.80 (Android; Opera Mini/7.6.40234/36.2592; U; ru) Presto/2.12.423 Version/12.16'
        req = make_mocked_request('GET', '/', headers={'User-Agent': ua}, transport=self.getTransport('77.244.121.69'))
        start = int(round(time.time() * 1000))
        parser = RequestParser(req, shash='fc0bbd68687f68b791690200c02a9534')
        time3 = int(round(time.time() * 1000)) - start
        assert parser.isValid()

        assert time1 > time2
        assert time3 > time2

    def test_chooser(self): # ассеты не нужны т.к. тестовые данные не стабильны и результат можнет меняться, тут проверка что хоть не падает ничего
        self.cleanRedis()

        ua = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-T116 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 YaBrowser/15.2.2214.3725.01 Safari/537.36'

        # тест агрегаторов для 24 оператора
        req = make_mocked_request('GET', '/',
                                  headers={'User-Agent': ua},
                                  transport=self.getTransport('217.118.90.248'))
        parser = RequestParser(req, shash='8e98a514ff1957cf3148617c1e7e0cd1')  # 1146 stream 4122 split
        land = LandChooser(parser).getLanding()

        # для 32 оператора
        req = make_mocked_request('GET', '/',
                                  headers={
                                      'User-Agent': ua,
                                      'HTTP_REFERER': 'https://vk.com/mikhailkharchev',
                                      'COOKIE': '8e98a514ff1957cf3148617c1e7e0cd1_d2b6043e84b2aebc95a2faf382bde230=1'
                                  },
                                  transport=self.getTransport('85.26.165.231'))
        parser = RequestParser(req, shash='8e98a514ff1957cf3148617c1e7e0cd1')  # 1146 stream 4123 split
        land = LandChooser(parser).getLanding()

        # для 25 оператора
        req = make_mocked_request('GET', '/',
                                  headers={
                                      'User-Agent': ua,
                                      'HTTP_REFERER': 'https://vk.com/mikhailkharchev',
                                      'COOKIE': '8e98a514ff1957cf3148617c1e7e0cd1_d2b6043e84b2aebc95a2faf382bde230=2'
                                  },
                                  transport=self.getTransport('5.44.36.224'))
        parser = RequestParser(req, shash='8e98a514ff1957cf3148617c1e7e0cd1')  # 1146 stream 4124 split
        land = LandChooser(parser).getLanding()

        # указан лендос отсекающийся по стоп словам
        req = make_mocked_request('GET', '/?landing=300',
                                  headers={
                                      'User-Agent': ua,
                                  },
                                  transport=self.getTransport('5.44.36.224'))
        parser = RequestParser(req, shash='f73808916168e460c5378cc4cbf996df')  # 1145 stream
        land = LandChooser(parser).getLanding()

        # сохранение SubId для результата
        req = make_mocked_request('GET', '/?landing=214',
                                  headers={
                                      'User-Agent': ua,
                                  },
                                  transport=self.getTransport('85.26.165.231'))
        parser = RequestParser(req, shash='0874b8e9a74d0119155fac3306fecd24')  # 1143 stream
        land = LandChooser(parser).getLanding()

    def test_response(self):
        self.cleanRedis()

        ua = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-T116 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 YaBrowser/15.2.2214.3725.01 Safari/537.36'

        req = make_mocked_request('GET', '/',
                                  headers={'User-Agent': ua},
                                  transport=self.getTransport('217.118.90.248'))
        parser = RequestParser(req, shash='8e98a514ff1957cf3148617c1e7e0cd1')  # 1146 stream 4122 split

        landing = json.loads(DbHelper().getFrom('TDSLand', '383').decode())
        response = PreparatoryResponse(parser, landing).getResponse()
        assert isinstance(response, web.Response)
        assert DbHelper().get('linkFreshesAD:'+parser.uniqHash)
        DbHelper().delete('linkFreshesAD:'+parser.uniqHash)

        landing = json.loads(DbHelper().getFrom('TDSLand', '383').decode())
        response = PreparatoryResponse(parser, landing, direct=True).getResponse()
        assert isinstance(response, web.HTTPPermanentRedirect)
        assert DbHelper().get('LinkFreshesPreland:'+parser.uniqHash)
        DbHelper().delete('LinkFreshesPreland:'+parser.uniqHash)

        response = PreparatoryResponse(parser, False).getResponse()
        assert isinstance(response, web.HTTPPermanentRedirect)
        assert not DbHelper().get('linkFreshesAD:'+parser.uniqHash)

    def getTransport(self, ip):
        transport = mock.Mock()

        def get_extra_info(key):
            if key == 'peername':
                return [ip, 80]
            else:
                return None

        transport.get_extra_info.side_effect = get_extra_info

        return transport

    def cleanBases(self):
        self.cleanRedis()

        DeviceModelList.truncate_table()
        OSList.truncate_table()
        BrowserList.truncate_table()
        VendorList.truncate_table()
        OSVersionList.truncate_table()
        CountryList.truncate_table()

    def cleanRedis(self):
        DbHelper().delete('VendorList', 'TDSStream', 'NormalBrowserList', 'CountryList', 'TDSSplit',
                           'TDSSourceList', 'DeviceModelList', 'GlobalSettings', 'OSVersionList', 'NormalOSList',
                          'AgregatorList', 'BadRefererList', 'StopWords', 'TDSLand')

    def ttest_forfun(self):  # использовался для разработки
        self.cleanRedis()
        ua = 'Mozilla/5.0 (Linux; Android 4.4.4; SM-T116 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 YaBrowser/15.2.2214.3725.01 Safari/537.36'
