import redis
import json
from dbModels import *
from config import redisConfig
from datetime import datetime
import os
from .Singleton import Singleton

if os.environ.get('RUN_MOD') == 'TEST':
    config = redisConfig['test']
else:
    config = redisConfig['main']


class DbHelper(metaclass=Singleton):
    redis = None
    updaters = {}

    def __init__(self):
        self.redis = redis.Redis(**config['connect'])
        self.updaters = {
            'NormalOSList': self.updateOsList,
            'OSVersionList': self.updateOSVersionList,
            'VendorList': self.updateVendorList,
            'NormalBrowserList': self.updateBrowserList,
            'DeviceModelList': self.updateDeviceModelList,
            'CountryList': self.updateCountryList,

            'TDSSourceList': self.updateTDSSourceList,
            'TDSStream': self.updateTDSStream,
            'TDSSplit': self.updateTDSSplit,
            'TDSLand': self.updateTDSLand,
            'AgregatorList': self.updateAgregatorList,

            'PrelandUserOperatorSettings': self.updatePrelandUserOperatorSettings,
            'PrelandStreamOperatorSettings': self.updatePrelandStreamOperatorSettings,
            'PrelandUserReferrerSettings': self.updatePrelandUserReferrerSettings,

            'BadRefererList': self.updateBadReferers,
            'StopWords': self.updateStopWords,
            'GlobalSettings': self.updateGlobalSettings,
        }

    def updateRedisData(self, name):
        if name in self.updaters:
            return self.updaters[name]()

        return False

    def get(self, name):
        if self.redis.exists(name) or self.updateRedisData(name):
            if self.redis.type(name) == b'hash':
                value = self.redis.hgetall(name)
            else:
                value = self.redis.get(name)
        else:
            value = 0
        return value

    def getFrom(self, name, key):
        value = self.redis.hget(name, key)  # self.get(name)
        if not self.redis.exists(name) or not value:
            self.updateRedisData(name)
            value = self.redis.hget(name, key)
        return value

    def setTo(self, name, key, value):
        self.redis.hset(name, key, value)

    def set(self, name, value):
        self.redis.set(name, value)

    def setAndExpire(self, key, value, seconds):
        self.redis.set(key, value)
        self.redis.expire(key, seconds)

    def delete(self, *names):
        self.redis.delete(*names)

    def increment(self, name):
        if self.redis.exists(name):
            self.redis.incr(name, 1)

    def incAggregatorRequestsCount(self, id):
        date = datetime.now()
        name = 'AgregatorsRequestCount_' + date.strftime("%Y%m%d") + ':' + str(id)
        if self.redis.exists(name):
            self.redis.incr(name, 1)
        else:
            self.setAndExpire(name, 1, 60*60*24*7)

    # дальше идут обновляторы для таблиц
    def updateOsList(self):
        temp = {}
        for os in OSList.select(OSList.name, OSList.os_id):
            temp[os.name] = os.os_id

        if len(temp):
            self.redis.hmset('NormalOSList', temp)

        return temp

    def updateOSVersionList(self):
        temp = {}
        for osVersion in OSVersionList.select(OSVersionList.os_id):
            if osVersion.os_id not in temp:
                temp20 = []
                for versionByOs in OSVersionList.select(OSVersionList.os_version_id, OSVersionList.name, OSVersionList.os_id).where(OSVersionList.os_id == osVersion.os_id):
                    temp20.append(versionByOs.toDict())
                temp[osVersion.os_id] = json.dumps(temp20)

        if len(temp):
            self.redis.hmset('OSVersionList', temp)
        return temp

    def updateVendorList(self):
        temp = {}
        for vendor in VendorList.select(VendorList.name, VendorList.vendor_id):
            temp[vendor.name] = vendor.vendor_id

        if len(temp):
            self.redis.hmset('VendorList', temp)
        return temp

    def updateBrowserList(self):
        temp = {}
        for browser in BrowserList.select(BrowserList.browser_id, BrowserList.name):
            temp[browser.name] = browser.browser_id

        if len(temp):
            self.redis.hmset('NormalBrowserList', temp)
        return temp

    def updateDeviceModelList(self):
        temp = {}
        for model in DeviceModelList.select(DeviceModelList.vendor_id):
            if model.vendor_id not in temp:
                temp20 = []
                for modelByVendor in DeviceModelList.select(DeviceModelList.device_model_id, DeviceModelList.name, DeviceModelList.vendor_id)\
                        .where(DeviceModelList.vendor_id == model.vendor_id):
                    temp20.append(modelByVendor.toDict())
                temp[model.vendor_id] = json.dumps(temp20)

        if len(temp):
            self.redis.hmset('DeviceModelList', temp)
        return temp

    def updateCountryList(self):
        temp = {}
        for country in CountryList.select(CountryList.isoCode, CountryList.country_id):
            temp[country.isoCode] = country.country_id

        if len(temp):
            self.redis.hmset('CountryList', temp)
        return temp

    def updateTDSSourceList(self):
        temp = {}
        for stream in TDSStream.select():
            temp[stream.hash] = stream.id_stream

        if len(temp):
            self.redis.hmset('TDSSourceList', temp)
        return temp

    def updateTDSStream(self):
        temp = {}
        for stream in TDSStream.select():
            temp[stream.id_stream] = json.dumps(stream.toDict())

        if len(temp):
            self.redis.hmset('TDSStream', temp)
        return temp

    def updateTDSSplit(self):
        temp = {}
        for split in TDSSplit.select():
            temp[str(split.stream_id) + '_' + str(split.split_order)] = json.dumps(split.toDict())

        if len(temp):
            self.redis.hmset('TDSSplit', temp)
        return temp

    def updateTDSLand(self):
        temp = {}
        for land in TDSLand.select():
            temp[land.id_land] = json.dumps(land.toDict())

        if len(temp):
            self.redis.hmset('TDSLand', temp)
        return temp

    def updateAgregatorList(self):
        temp = {}
        for agregator in AgregatorList.select():
            temp[agregator.agregator_id] = json.dumps(agregator.toDict())

        if len(temp):
            self.redis.hmset('AgregatorList', temp)
        return temp

    def updatePrelandUserOperatorSettings(self):
        temp = {}
        for preland in OperatorUserPreland.select():
            temp[str(preland.user_id) + '_' + str(preland.operator_id)] = preland.value

        if len(temp):
            self.redis.hmset('PrelandUserOperatorSettings', temp)
        return temp

    def updatePrelandStreamOperatorSettings(self):
        temp = {}
        for preland in OperatorStreamPreland.select():
            temp[str(preland.stream_id) + '_' + str(preland.operator_id)] = preland.value

        if len(temp):
            self.redis.set('PrelandStreamOperatorSettings', temp)
        return temp

    def updatePrelandUserReferrerSettings(self):
        temp = {}
        for user in Users.select():
            if user.prelands_json_referer != '':
                temp[user.id] = user.prelands_json_referer

        if len(temp):
            self.redis.set('PrelandUserReferrerSettings', temp)
        return temp

    def updateBadReferers(self):
        referers = []
        for ref in BadReferersList.select().where(BadReferersList.type == 'referer'):
            referers.append(ref.value)

        if len(referers):
            self.redis.set('BadRefererList', json.dumps(referers))
        return referers

    def updateStopWords(self):
        words = []
        for ref in BadReferersList.select().where(BadReferersList.type == 'stopword'):
            words.append(ref.value)

        if len(words):
            self.redis.set('StopWords', json.dumps(words))
        return words

    def updateGlobalSettings(self):
        settings = {}
        for option in GlobalSettings.select():
            settings = option.toDict()

        if len(settings):
            self.redis.set('GlobalSettings', json.dumps(settings))
        return settings

    def checkMysql(self):
        if not db.get_conn().ping():
            return False
        return True

    def checkRdis(self):
        if not self.redis.ping():
            return False
        return True


