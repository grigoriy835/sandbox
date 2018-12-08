from helpers import DbHelper, SmartRotatorHelper, AgregatorRegister, LogHelper
from .RequestParser import RequestParser
import asyncio
from aiohttp import ClientSession
import json
import random
from concurrent.futures import CancelledError
import sys, traceback


class LandChooser:
    parsedRequest = None  # type: RequestParser
    resultLanding = None
    validLands = None
    agregators = None

    landRatings = None
    landResults = None
    future = None
    session = None

    def __init__(self, parsedRequest):
        self.parsedRequest = parsedRequest
        self.validLands = {}
        self.landRatings = {}
        self.landResults = {}
        self.agregators = {}

    async def getLanding(self):
        archetypalLands = []
        if self.resultLanding is None and self.parsedRequest.isValid():
            if self.parsedRequest.chosenLand:
                landing = json.loads(DbHelper().getFrom('TDSLand', self.parsedRequest.chosenLand).decode())
                archetypalLands.append(landing)
            else:
                for landId in self.parsedRequest.split['land_array']:
                    landing = json.loads(DbHelper().getFrom('TDSLand', landId).decode())
                    archetypalLands.append(landing)

            for landing in archetypalLands:
                if self.checkLanding(landing):
                    self.validLands[landing['id_land']] = landing

            if len(self.validLands):
                await self.determineLandRatings()
                await self.findBestLand()
            else:
                self.resultLanding = False
        data = {
            'lands': len(archetypalLands),
            'valid_lands': str(self.validLands.keys()),
            'agregators': str(self.agregators),
            'ratings': str(self.landRatings),
            'results': str(self.landResults),
            'finally': str(self.resultLanding['id_land']) if self.resultLanding else None,
        }
        LogHelper().infoMessage('chooser_log', 'done for hash: ' + str(self.parsedRequest.uniqHash) + ' data: ' + str(data))
        return self.resultLanding

    def checkLanding(self, landing):
        if landing['disabled']:
            return False

        if landing['id_operator'] != self.parsedRequest.operatorId:
            return False

        # if landing['id_agregator'] != 8:  # debug
        #     return False

        landing['device_type'] = json.loads(landing['device_type'])
        if str(self.parsedRequest.type) not in landing['device_type']:
            return False

        if landing['os_array'] != 'all':
            landing['os_array'] = json.loads(landing['os_array'])
            if landing['os_equal_type'] == 'equal':
                if self.parsedRequest.osId not in landing['os_array']:
                    return False
            else:
                if self.parsedRequest.osId in landing['os_array']:
                    return False

        if landing['browser_array'] != 'all':
            landing['browser_array'] = json.loads(landing['browser_array'])
            if landing['browser_equal_type'] == 'equal':
                if self.parsedRequest.osId not in landing['os_array']:
                    return False
            else:
                if self.parsedRequest.osId in landing['os_array']:
                    return False

        if landing['user_agent_ex'] != "" and landing['user_agent_ex'] != "[]":
            stopWords = json.loads(landing['user_agent_ex'] if landing['user_agent_ex'] else '[]')

            lowerAgent = self.parsedRequest.userAgent.lower()
            for word in stopWords:
                if word in lowerAgent:
                    return False

        return True

    async def determineLandRatings(self):
        if len(self.validLands) == 1:
            self.landRatings[0] = next(iter(self.validLands.keys()))
            return

        stream = self.parsedRequest.stream
        # if 'enable_smart_rotator' in stream and stream['enable_smart_rotator']:
        #     self.landRatings = await SmartRotatorHelper.getRatingsByLands(self.validLands, self.parsedRequest)

        if 0 not in self.landRatings:
            ratings = list(range(0, len(self.validLands)))
            random.shuffle(ratings)
            for id_land in self.validLands:
                self.landRatings[ratings.pop()] = id_land

        for land in self.validLands.keys():
            if land not in self.landRatings.values():
                ratings = list(range(0, len(self.validLands)))
                random.shuffle(ratings)
                for id_land in self.validLands:
                    self.landRatings[ratings.pop()] = id_land
                break

    async def findBestLand(self):
        async with ClientSession() as self.session:
            tasks = []
            for id_land in self.validLands:
                tasks.append(self.determineLandUrl(self.validLands[id_land]))

            self.future = asyncio.gather(*tasks)

            try:
                await self.future
            except CancelledError:
                pass

        self.session.close()
        if self.resultLanding is None:
            self.resultLanding = False

    async def determineLandUrl(self, landing):
        id_land = landing['id_land']
        agregator = json.loads(DbHelper().getFrom('AgregatorList', landing['id_agregator']).decode())

        if (agregator['handler'] is None or agregator['handler'] is '') and landing['land_url'] is not None:
            self.landResults[id_land] = {'url': landing['land_url']}
        elif agregator['handler'] in AgregatorRegister.REGISTRY:
            self.agregators[id_land] = agregator['handler']
            result = await AgregatorRegister.REGISTRY[agregator['handler']].getLandingUrl(landing, self.parsedRequest, self.session)
            if result and 'PTError' in result:
                self.parsedRequest.hasPaymentToolsError = True
            if result and 'url' in result:
                if 'subId' in result:
                    result['handler'] = agregator['handler']
            self.landResults[id_land] = result
        else:
            self.landResults[id_land] = False

        # смотрим, можем ли мы вернуть результат уже сейчас
        for rating in sorted(self.landRatings.keys()):
            if self.landRatings[rating] in self.landResults:
                if self.landResults[self.landRatings[rating]]:
                    self.completeDefinition('by_land')
            else:
                return

    def completeDefinition(self, *args):
        for key in sorted(self.landRatings.keys()):
            if self.landRatings[key] in self.landResults and self.landResults[self.landRatings[key]]:
                id_land = self.landRatings[key]
                result = self.landResults[id_land]
                self.resultLanding = self.validLands[id_land]
                self.resultLanding['land_url'] = result['url']
                if 'subId' in result:
                    AgregatorRegister.REGISTRY[result['handler']].saveSubId(self.parsedRequest.uniqHash, result['subId'])
                break

        self.session.close()
        self.future.cancel()
