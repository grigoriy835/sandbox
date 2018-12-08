from config import agregatorsUrl, appConfig
import json
from .AgregatorRegister import AgregatorRegister
from .Base import Base
from helpers.LogHelper import LogHelper
from asyncio import CancelledError
from helpers.DbHelper import DbHelper


class NMSHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 7

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        if parsedRequest.operatorId == 32:
            url = agregatorsUrl['NMS'][32]
            data = json.dumps({
                'client_id': '106',
                'service_id': landing['bakcell_service_id'],
                'url': 'http://' + appConfig['aggregator_receiver_host'] + '/azercell_subscribe?uniq_hash=' + parsedRequest.uniqHash,
                'reject_url': 'http://' + appConfig['aggregator_receiver_host'] + '/azercell_subscribe_reject?uniq_hash=' + parsedRequest.uniqHash,
            })
        else:
            url = agregatorsUrl['NMS']['other']
            data = json.dumps({
                'client_id': '106',
                'service_id': landing['bakcell_service_id'],
                'landing_id': landing['bakcell_landing_id'],
                'url': 'http://' + appConfig['aggregator_receiver_host'] + '/receive_bakcell?uniq_hash=' + parsedRequest.uniqHash,
                'reject_url': 'http://' + appConfig['aggregator_receiver_host'] + '/reject_bakcell?uniq_hash=' + parsedRequest.uniqHash,
            })

        for i in range(3):
            try:
                async with session.post(url, data=data, timeout=6) as request:
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
            'request': str(data),
            'response': str(response),
        }
        LogHelper().infoMessage('agregators/NMS_log', str(logData))
        try:
            response = json.loads(response)
        except Exception:
            cls.storeError(data, response, 'cant parse response')
            return False

        DbHelper().incAggregatorRequestsCount(cls.agregatorId)

        if response and 'redirect_url' in response:
            result = {
                'url': response['redirect_url']
            }
        else:
            result = False

        return result
