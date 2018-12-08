from hashlib import md5
import uuid

from config import agregatorsUrl
from helpers.LogHelper import LogHelper
from .AgregatorRegister import AgregatorRegister
from .Base import Base
from asyncio import CancelledError
from helpers.DbHelper import DbHelper


class PaymentToolsHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 12

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        post = {
            'service_id': landing['ptools_service_id'],
            'pid': parsedRequest.uniqHash,
            'ip': parsedRequest.ip,
            'ua': parsedRequest.userAgent,
            'redirect_url': landing['prools_redirect_url'],
        }
        if 'ptools_tmpl' in landing and landing['ptools_tmpl']:
            post['tmpl'] = landing['ptools_tmpl']

        data = ''
        for key in sorted(post):
            data += str(post[key])
        data += landing['ptools_secret_key']

        post['sign'] = md5(data.encode()).hexdigest()

        url = agregatorsUrl['PaymentTools']

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

        if 'PTError' in result:
            LogHelper().infoMessage('agregators/PT_Error.log', parsedRequest.uniqHash + ': error, another one')
            post = {
                'service_id': landing['ptools_service_id'],
                'pid': uuid.uuid4().hex,
                'ip': parsedRequest.ip,
                'ua': parsedRequest.userAgent,
                'redirect_url': landing['prools_redirect_url'],
            }
            if 'ptools_tmpl' in landing and landing['ptools_tmpl']:
                post['tmpl'] = landing['ptools_tmpl']

            data = ''
            for key in sorted(post):
                data += str(post[key])
            data += landing['ptools_secret_key']

            post['sign'] = md5(data.encode()).hexdigest()

            url = agregatorsUrl['PaymentTools']

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

            LogHelper().infoMessage('agregators/PT_Error.log', parsedRequest.uniqHash + ': ' + str(result))

        logData = {
            'request': str(post),
            'response': str(response),
            'result': str(result)
        }
        LogHelper().infoMessage('agregators/PaymentTools_log', str(logData))

        DbHelper().incAggregatorRequestsCount(cls.agregatorId)

        if 'error' in result:
            cls.storeError(post, response, result['error'])
            result = False

        return result

    @staticmethod
    def parseResponse(response):
        if isinstance(response, type('')):
            if 'Redirect' in response:
                return {
                    'url': response[response.find('Redirect')+9:],
                }
            if '!DOCTYPE html' in response or '!doctype html' in response:
                return {
                    'PTError': True,
                    'error': 'type of response not correct (HTML)'
                }

        return {
            'error': 'no error description in response'
        }

    @staticmethod
    def saveSubId(hash, subId):
        pass
