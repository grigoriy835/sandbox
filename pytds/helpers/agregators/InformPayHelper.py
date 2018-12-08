from hashlib import md5
from urllib import parse
from helpers.LogHelper import LogHelper
from asyncio import CancelledError

from config import agregatorsUrl
from .AgregatorRegister import AgregatorRegister
from .Base import Base
import time
from helpers.DbHelper import DbHelper


class InformPayHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 14

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        post = None
        if parsedRequest.operatorId in agregatorsUrl['InformPay']:
            url = agregatorsUrl['InformPay'][parsedRequest.operatorId]
        else:
            return False

        hash = md5((landing['informpay_service_code'] + parsedRequest.uniqHash + parsedRequest.ip
                   + landing['informpay_return_url'] + landing['informpay_salt']).encode()).hexdigest()
        url += 'service_code=' + landing['informpay_service_code'] + '&partner_key=' + parsedRequest.uniqHash + '&return_url=' \
               + parse.quote_plus(landing['informpay_return_url']) + '&hash=' + hash + '&ip=' + parsedRequest.ip

        if landing['informpay_landing_id']:
            url += '&landing=' + landing['informpay_landing_id']

        if landing['informpay_ic_landing_id']:
            url += '&iclanding=' + landing['informpay_ic_landing_id']

        url += '&cs1=77'

        start = int(time.time())
        LogHelper().infoMessage('agregators/informPay_log', 'start with hash:' + str(parsedRequest.uniqHash))
        for i in range(3):
            try:
                async with session.get(url, timeout=5) as request:
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

        DbHelper().incAggregatorRequestsCount(cls.agregatorId)

        logData = {
            'request': str(url),
            'response': str(response),
            'result': str(result),
            'duration': int(time.time() - start)
        }
        LogHelper().infoMessage('agregators/informPay_log', str(logData))

        if 'error' in result:
            cls.storeError(url, response, result['error'])
            result = False

        return result

    @staticmethod
    def parseResponse(response):
        statusOKPosition = response.find('<status>ok</status>')
        urlPositionStart = response.find('<tmp_link>')

        if statusOKPosition > 0 and urlPositionStart > 0:
            result = {
                'url': response[urlPositionStart+10:response.find('</tmp_link>')]
            }
        else:
            result = {
                'error': 'response not correct'
            }
        return result

    @staticmethod
    def saveSubId(hash, subId):
        pass
