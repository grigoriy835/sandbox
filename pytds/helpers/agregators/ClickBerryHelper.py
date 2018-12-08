import json
from datetime import datetime
from hashlib import md5
import time
from asyncio import CancelledError

from config import agregatorsUrl
from .AgregatorRegister import AgregatorRegister
from .Base import Base
from helpers.LogHelper import LogHelper
from helpers.DbHelper import DbHelper


class ClickBerryHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 18
    pid = '1'  # pid in clickberry.xyz
    secretKey = 'qvhtlnywsu'

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        post = {
            'pid': cls.pid,
            'sid': landing['clickberry_sid'],
            'hash': landing['clickberry_hash'],
            'ip': parsedRequest.ip,
            'useragent': parsedRequest.userAgent,
            'date': date,
            'prelend': 1 if (parsedRequest.useprlp == '1') else 0,
            'signature': md5((cls.pid + str(landing['clickberry_sid']) + date + landing['clickberry_hash']).encode()).hexdigest(),
            'sub_1': parsedRequest.uniqHash,
        }

        url = agregatorsUrl['ClickBerry']

        start = int(time.time())
        LogHelper().infoMessage('agregators/ClickBerry_log', 'start with hash:' + str(parsedRequest.uniqHash))
        for i in range(3):
            try:
                async with session.post(url, data=post, timeout=5) as request:
                    response = await request.text()
                    break
            except CancelledError:
                if i == 2:
                    response = 'CancelledError'
                    break
            except RuntimeError:
                return False
            except Exception as e:
                response = str(type(e))
                break

        logData = {
            'request': str(post),
            'response': str(response),
            'duration': int(time.time()-start)
        }
        LogHelper().infoMessage('agregators/ClickBerry_log', str(logData))

        DbHelper().incAggregatorRequestsCount(cls.agregatorId)
        try:
            result = cls.parseResponse(response)
        except Exception:
            result = {
                'error': 'error processing parse response'
            }

        if 'error' in result:
            cls.storeError(post, response, result['error'])
            result = False

        return result

    @staticmethod
    def parseResponse(agregatorResponse):
        try:
            response = json.loads(agregatorResponse)
        except Exception:
            return {
                'error': 'cant parse response(('
            }
        result = {}
        if 'message' in response and response['message'] == 'ok':
            if 'link' in response:
                result['url'] = response['link']
            else:
                result['error'] = 'Have not link in response'
        elif 'message' in response:
            result['error'] = response['message']
        else:
            result['error'] = 'Unknown'

        return result

    @staticmethod
    def saveSubId(hash, subId):
        pass
