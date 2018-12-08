import xml.etree.ElementTree as ET
from datetime import datetime
from hashlib import md5

from config import agregatorsUrl
from helpers.ViewHelper import view
from .AgregatorRegister import AgregatorRegister
from .Base import Base
from dbModels import PlanetSubsId
from asyncio import CancelledError
from helpers.DbHelper import DbHelper


class PlanetThreeICHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 6

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        data = {
            'ip': parsedRequest.ip,
            'project_id': landing['planet_project_id'],
            'login': landing['planet3_ic_login'],
            'password': landing['planet3_ic_password'],
            'network_id': landing['planet3_ic_network_id'],
            'amount': landing['planet3_ic_amount'],
            'now': datetime.now().strftime("%Y%m%d%H%M%S"),
            'uniq_hash': parsedRequest.uniqHash
        }
        data['signature'] = md5(
            (data['login']+md5((data['now']+data['password']).encode()).hexdigest()).encode()
        ).hexdigest()

        post = view('agregators/PlanetThreeIC.xml', data)

        url = agregatorsUrl['PlanetThreeIC']

        for i in range(3):
            try:
                async with session.post(url, data=post, headers={'Service-Method': 'CreateInvoice'}, timeout=6) as request:
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
    def parseResponse(response):
        try:
            e = ET.fromstring(response)
        except Exception:
            return {
                'error': 'cant parse response(('
            }

        if e.find('ResultCode') and int(e.find('ResultCode').text) is 0:
            return {
                'url': e.find('AuthorizationUrl').text,
                'subId': e.find('InvoiceID').text,
            }
        else:
            return {
                'error': e.find('ResultDescription').text
            }

    @staticmethod
    def saveSubId(hash, subId):
        PlanetSubsId.insert(uniq_hash=hash, sub_id=subId)
