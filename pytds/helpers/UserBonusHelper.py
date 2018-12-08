from helpers import DbHelper
from helpers.LogHelper import LogHelper
import asyncio
from aiohttp import ClientSession
from config import appConfig
from hashlib import md5


class UserBonusHelper:
    secret_key = 'SMOKEweedEVRYDAY'

    @classmethod
    def checkBonusEvent(cls, parsedRequest):
        event = DbHelper().get('UserBonusEvents:'+str(parsedRequest.stream['id_partner']))
        if event and DbHelper().get('userBonusEventNeedFirstSubscribe:'+str(parsedRequest.stream['id_stream'])):
            asyncio.get_event_loop().create_task(cls.createBonusEventItems(parsedRequest))

    @classmethod
    async def createBonusEventItems(cls, parsedRequest):
        data = {
            'stream_id': parsedRequest.stream['id_stream'],
            'partner_id': parsedRequest.stream['id_partner'],
            'key': parsedRequest.uniqHash
        }
        LogHelper().infoMessage('bonus_event_log', 'Event: ' + str(data))
        data['hash'] = md5((data['key'] + cls.secret_key).encode()).hexdigest()
        async with ClientSession() as session:
            async with session.post('http://'+appConfig['aggregator_receiver_host'] + '/add_bonus_sub', data=data) as request:
                response = await request.text()
