from config import rotatorConfig
import os
import json
from helpers import LogHelper
from aiohttp import ClientSession
import asyncio

# если не боевой запуск то выдёргивает конфиг с тестовым окружением
if os.environ.get('RUN_MOD') == 'TEST':
    config = rotatorConfig['test']
else:
    config = rotatorConfig['main']


class SmartRotatorHelper:
    @classmethod
    async def getRatingsByLands(cls, landings, parsedRequest):
        stream = parsedRequest.stream

        streamHash = cls._countStreamHash(parsedRequest)

        if int(stream['enable_smart_rotator']) is 1:
            params = [streamHash]
            response = await cls._executeRequest('mabserver.pure_bandit', params)
            request = ['mabserver.pure_bandit', params]
        else:
            params = [streamHash, [parsedRequest.hoursId, parsedRequest.operator.id, parsedRequest.browser]]
            response = await cls._executeRequest('mabserver.get_land_ef', params)
            request = ['mabserver.get_land_ef', params]

        LogHelper().infoMessage('smart_rotator', 'hash: ' + parsedRequest.uniqHash + ' Request: ' + json.dumps(request) + '; Response: ' + json.dumps(response))

        if 'error' in response:
            return {}

        if isinstance(response, type({})) and 'result' in response:
            response = response['result']

        conformityArray = sorted(response, key=lambda item: item[1])

        ratings = {}
        for rating in range(0, len(conformityArray)):
            ratings[rating] = conformityArray.pop()[0]

        return ratings

    @classmethod
    def incrementValue(cls, parsedRequest, landing):
        streamHash = cls._countStreamHash(parsedRequest)
        params = [streamHash, landing['id_land']]
        LogHelper().infoMessage('smart_rotator', 'incValue for hash: ' + parsedRequest.uniqHash)
        asyncio.get_event_loop().create_task(cls._executeRequest('mabserver.inc_n', params))

    @staticmethod
    def _countStreamHash(parsedRequest):
        streamHash = int(parsedRequest.stream['id_stream']) * 1000000 + int(parsedRequest.operator.operator_id) * 100\
                     + int(parsedRequest.cookieValue)
        return streamHash

    @staticmethod
    async def _executeRequest(method, params):
        headers = {'content-type': 'application/json'}
        request = {
            'jsonrpc': "2.0",
            'id': 0,
            'method': method,
            'params': params
        }
        try:
            async with ClientSession() as session:
                async with session.post(config['smartRotatorUrl'], data=json.dumps(request), headers=headers, timeout=1) as request:
                    response = await request.json()
        except asyncio.TimeoutError:
            LogHelper().infoMessage('smart_rotator',
                                    'TimeoutError: ' + json.dumps(request))
            response = ''
        except asyncio.CancelledError:
            LogHelper().infoMessage('smart_rotator',
                                    'CanceledError: ' + json.dumps(request))
            response = ''

        return response

    @classmethod
    async def checkRotator(cls):
        if not await cls._executeRequest('mabserver.helpmsg', []):
            return False
        return True
