from datetime import datetime
from hashlib import md5
import xml.etree.ElementTree as ET

from config import agregatorsUrl
from helpers.ViewHelper import view
from .AgregatorRegister import AgregatorRegister
from .Base import Base
from dbModels import PlanetSubsId
from asyncio import CancelledError
from helpers.DbHelper import DbHelper


class PlanetThreeHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 4
    secretKey = 'qoRiJykQ'

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        data = {
            'ip': parsedRequest.ip,
            'subscriptionProjectID': landing['planet_project_id'],
            'now': datetime.now().strftime("%Y%m%d%H%M%S"),
        }
        data['signature'] = md5((data['subscriptionProjectID']+data['now']+cls.secretKey).encode()).hexdigest().upper()

        post = view('agregators/PlanetThree.xml', data)

        url = agregatorsUrl['PlanetThree']

        for i in range(3):
            try:
                async with session.post(url, data=post, timeout=3) as request:
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

        if result and 'url' in result and parsedRequest.operatorId == 28 and landing['planet_mts_ext_lp_template']:
            result['url'] = result['url']+'?ext_lp_template='+landing['planet_mts_ext_lp_template']

        return result

    @staticmethod
    def parseResponse(response):
        try:
            e = ET.fromstring(response)
        except Exception:
            return {
                'error': 'cant parse response(('
            }

        if e.find('StatusName').text == 'REQUEST_ACCEPTED' and e.find('SubscriberAcceptanceChannel').text == 'AUTH_PAGE':
            return {
                'url': e.find('AuthorizeUrl').text,
                'subId': e.find('SubscriptionID').text,
            }
        elif e.find('ErrorDescription'):
            return {
                'error': e.find('ErrorDescription').text
            }

        return {
            'error': 'no error description in response'
        }

    @staticmethod
    def saveSubId(hash, subId):
        PlanetSubsId.insert(uniq_hash=hash, sub_id=subId)











