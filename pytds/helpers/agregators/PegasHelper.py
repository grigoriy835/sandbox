from .AgregatorRegister import AgregatorRegister
from helpers.LogHelper import LogHelper
from config import agregatorsUrl
from datetime import datetime
import json
from .Base import Base
from hashlib import md5
import time
from asyncio import CancelledError
from helpers.DbHelper import DbHelper


class PegasHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 11
    secretKey = 'NNbiolPOEmbgmyirtuf74Njf'
    pid = '95'

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        post = {
            'pid': cls.pid,
            'service_id': landing['pegas_service_id'],
            'hash': landing['pegas_service_hash'],
            'ip': parsedRequest.ip,
            'useragent': parsedRequest.userAgent,
            'date': datetime.now().strftime("%Y%m%d%H%M%S"),
            'signature': md5((cls.pid + str(landing['pegas_service_id'])+datetime.now().strftime("%Y%m%d%H%M%S")+landing['pegas_service_hash']).encode()).hexdigest(),
            'sub_1': parsedRequest.uniqHash
        }

        url = agregatorsUrl['Pegas']

        start = int(time.time())
        LogHelper().infoMessage('agregators/pegas_log', 'start with hash:' + str(parsedRequest.uniqHash))
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

        try:
            result = cls.parseResponse(response)
        except Exception:
            result = {
                'error': 'error processing parse response'
            }

        logData = {
            'request': str(post),
            'response': str(response),
            'result': str(result),
            'duration': int(time.time()-start)
        }
        LogHelper().infoMessage('agregators/pegas_log', str(logData))

        DbHelper().incAggregatorRequestsCount(cls.agregatorId)

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

        if response and isinstance(response, type({})) and 'message' in response and response['message'] == 'ok':
            if 'link' in response:
                result = {
                    'url': response['link']
                }
            else:
                result = {
                    'error': 'Have not link in response'
                }
        else:
            if response and isinstance(response, type({})) and 'message' in response:
                result = {
                    'error': 'unknown'
                }
            else:
                result = {
                    'error': response['message']
                }

        return result

    @staticmethod
    def saveSubId(hash, subId):
        pass
