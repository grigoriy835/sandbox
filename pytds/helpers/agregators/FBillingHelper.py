from hashlib import sha256
import base64
import hmac
import json
import time
from asyncio import CancelledError

from config import agregatorsUrl
from .AgregatorRegister import AgregatorRegister
from .Base import Base
from helpers.DbHelper import DbHelper

from dbModels import FBillingSubsId


class FBillingHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 5

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        post = "service_id="+landing['fbilling_service_id']+"&order_id="+parsedRequest.uniqHash+"&ip="+parsedRequest.ip
        url = agregatorsUrl['FBilling']
        timestamp = str(int(time.time()))

        # тут мы получаем signature для хедеров
        signString = (landing['fbilling_service_id']+timestamp+'POST'+url+post)
        m = hmac.new(landing['fbilling_secret_key'].encode(), digestmod=sha256)
        m.update(signString.encode())
        hmacString = m.hexdigest()
        signature = base64.b64encode(hmacString.encode()).decode()
        # получили

        headers = {'Authorization': landing['fbilling_service_id']+':'+timestamp+':'+signature}

        for i in range(3):
            try:
                async with session.post(url, data=post, headers=headers, timeout=3) as request:
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
        if response and 'redirect_url' in response and 'subscription_id' in response:
            result['url'] = response['redirect_url']
            result['subId'] = response['subscription_id']
            return result
        result['error'] = 'have no redirect_url or subscription_id in response'

        return result

    @staticmethod
    def saveSubId(hash, subId):
        FBillingSubsId.insert(uniq_hash=hash, sub_id=subId)
