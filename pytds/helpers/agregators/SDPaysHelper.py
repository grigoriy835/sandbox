import re
from datetime import datetime
from hashlib import md5

from config import agregatorsUrl
from .AgregatorRegister import AgregatorRegister
from .Base import Base
from dbModels import SDPaysSubsId
from asyncio import CancelledError
from helpers.DbHelper import DbHelper


class SDPaysHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 3
    operators = {
        25: 'megafon',
        28: 'mts',
        24: 'beeline'
    }

    responseErrors = {
         '201': 'Wrong user_id',
         '202': 'Wrong project_id',
         '203': 'Wrong datetime',
         '204': 'Wrong md5hash',
         '205': 'Wrong back_url',
         '206': 'Wrong abonent_ip',
         '207': 'Wrong operator',
         '208': 'System error 208 (repeat request allowed)',
         '209': 'System error 209',
         '210': 'System error 210',
         '211': 'System error 211',
         '212': 'System error 212',
         '213': 'System error 213',
         '214': 'Wrong project',
         '215': 'Wrong md5_hash (215)',
         '216': 'Operator is not allowed',
         '217': 'Activation type is not allowed',
         '218': 'Too match requests on this ip',
         '219': 'System error 219',
         '220': 'Service unavailable',
         '221': 'Wrong service response 221',
         '222': 'MTS service not active',
         '223': 'Service error 223',
         '224': 'Wrong service response 224',
         '225': 'Wrong request 225',
    }

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        post = dict()
        post['user_id'] = '70022'
        post['project_id'] = str(landing['sdpays_project_id'])
        post['date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post['md5_hash'] = md5((post['project_id']+post['date_time']+landing['sdpays_project_md5']).encode()).hexdigest()
        post['back_url'] = landing['back_url']
        post['abonent_ip'] = parsedRequest.ip

        if parsedRequest.operatorId not in cls.operators:
            return False
        else:
            post['operator'] = cls.operators[parsedRequest.operatorId]

        url = agregatorsUrl['SDPays']

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

        return result

    @classmethod
    def parseResponse(cls, response):
        status, sub = re.search(r'<RESULT>(\d+):(\d+)</RESULT>', response).groups()

        if status in cls.responseErrors:
            return {
                'error': cls.responseErrors[response.text]
            }

        if status != '200':
            return {
                'error': 'status 200 not found in response'
            }

        url = re.search(r'<REDIRECT>(.+)</REDIRECT>', response).groups()[0]

        response = {
            'url': url
        }

        if 'sub' in locals():
            response['subId'] = sub

        return response

    @staticmethod
    def saveSubId(hash, subId):
        SDPaysSubsId.insert(uniq_hash=hash, sub_id=subId)
