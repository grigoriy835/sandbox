from helpers import SmartRotatorHelper, UserBonusHelper, DbHelper, view, LogHelper
from aiohttp import web
from config import appConfig
from dbModels import Traffic
import base64
import time
import random
import json
from urllib import parse


class PreparatoryResponse:
    parsedRequest = None
    landing = None
    direct = False

    prelandConfig = None
    globalSettings = None

    def __init__(self, parsedRequest, landing, direct=False):
        self.prelandConfig = {
            'enable': False,
            'url': ''
        }
        self.parsedRequest = parsedRequest
        self.landing = landing
        self.direct = direct
        self.globalSettings = type(self).getGlobalSettings()

    def getResponse(self):
        if self.landing:
            landUrl = self.landing['land_url'].replace('{click_id}', self.parsedRequest.uniqHash)
            self.landing['land_url'] = landUrl
            self.obtainPrelandConfig()
            UserBonusHelper.checkBonusEvent(self.parsedRequest)  # todo
            #SmartRotatorHelper.incrementValue(self.parsedRequest, self.landing)

            if self.direct:
                if self.prelandConfig['enable']:
                    prelandBackUrl = 'http://' + appConfig['host'] + '/redirect_to_land?to=' + self.parsedRequest.uniqHash
                    prelandUrl = self.prelandConfig['url'].replace('{url}', base64.b64encode(prelandBackUrl.encode()).decode())
                    dataForRedis = {
                        'land_url': landUrl,
                        'timestamp': int(time.time()),
                        'redirect_to': 'land',
                        'redirect_type': 'directLink'
                    }

                    DbHelper().setAndExpire('LinkFreshesPreland:'+self.parsedRequest.uniqHash, json.dumps(dataForRedis),300)
                    response = web.HTTPFound(prelandUrl)
                else:
                    response = web.HTTPFound(landUrl)
                response.headers['Cache-Control'] = 'no-cache'
            else:
                redirectType = self.getRedirectType()
                if self.prelandConfig['enable']:
                    prelandBackUrl = 'http://' + appConfig['host'] + '/redirect_to_land?to=' + self.parsedRequest.uniqHash
                    prelandUrl = self.prelandConfig['url'].replace('{url}', base64.b64encode(prelandBackUrl.encode()).decode())

                    dataForRedis = {
                        'preland_url': prelandUrl,
                        'land_url': landUrl,
                        'timestamp': int(time.time()),
                        'redirect_to': 'preland',
                        'redirect_type': 'script'
                    }
                else:
                    dataForRedis = {
                        'land_url': landUrl,
                        'timestamp': int(time.time()),
                        'redirect_to': 'preland',
                        'redirect_type': 'script'
                    }

                DbHelper().setAndExpire('linkFreshesAD:'+self.parsedRequest.uniqHash, json.dumps(dataForRedis), 300)

                redirectUrl = 'http://' + appConfig['host'] + '/redirect?to=' + self.parsedRequest.uniqHash
                if redirectType == 1:
                    scriptBody = view('js/redirect.js', {'url': redirectUrl})
                elif redirectType == 2:
                    scriptBody = view('js/clickunder.js', {'url': redirectUrl})
                elif redirectType == 3:
                    scriptBody = view('js/blind.js', {'url': redirectUrl})
                elif redirectType == 4:
                    if self.landing['alert_phrases']:
                        phrases = json.dumps(self.landing['alert_phrases'])
                        phrase = random.choice(phrases.values())
                    else:
                        phrase = self.globalSettings['default_confirm_phrase']

                    scriptBody = view('js/confirm.js', {'url': redirectUrl, 'phrase': phrase})
                elif redirectType == 10:
                    expireTime = time.strftime('%a, %d-%b-%Y %H:%M:%S', time.localtime(time.time() + self.parsedRequest.cookiesLiveTime))
                    scriptBody = view('js/user_php_script.js', {
                        'url': redirectUrl,
                        'cookie': self.parsedRequest.cookieValue,
                        'cookieName': self.parsedRequest.cookieName,
                        'cookieTime': expireTime,
                    })
                else:
                    scriptBody = ''

                response = web.Response(text=scriptBody)

            response.set_cookie(self.parsedRequest.cookieName, self.parsedRequest.cookieValue, max_age=self.parsedRequest.cookiesLiveTime)
            response.set_cookie(self.parsedRequest.cookieName + '_datetime', self.parsedRequest.datetime, max_age=self.parsedRequest.cookiesLiveTime)

        else:
            tbUrl = self.globalSettings['global_tb_url']
            if self.parsedRequest.stream:
                tbUrl = self.parsedRequest.stream['tb_url']
            if self.parsedRequest.hasPaymentToolsError and 'payment_tools_tb_url' in self.globalSettings and self.globalSettings['payment_tools_tb_url']:
                tbUrl = str(self.globalSettings['payment_tools_tb_url']).replace('{tburl}', parse.quote_plus(tbUrl))
            response = web.HTTPFound(tbUrl)
            response.headers['Cache-Control'] = 'no-cache'

            if self.parsedRequest.stream:
                response.set_cookie(self.parsedRequest.cookieName, self.parsedRequest.cookieValue, max_age=self.parsedRequest.cookiesLiveTime)
                response.set_cookie(self.parsedRequest.cookieName + '_datetime', self.parsedRequest.datetime, max_age=self.parsedRequest.cookiesLiveTime)

        work_data = {
            'uniqHash': self.parsedRequest.uniqHash,
            'request_valid': self.parsedRequest.isValid(),
            'ip': self.parsedRequest.ip,
            'operatorId': self.parsedRequest.operatorId,
            'id_stream': self.parsedRequest.stream['id_stream'] if self.parsedRequest.stream else None,
            'split': self.parsedRequest.split['split_order'] if self.parsedRequest.split else None,
            'landing_id': self.landing['id_land'] if self.landing else None,
            'preland_status': 'enable' if self.prelandConfig['enable'] else 'disable',
            'preland_location': self.prelandConfig['url'] if self.prelandConfig['enable'] else None,
            'location': response.location if hasattr(response, 'location') else None,
        }
        LogHelper().infoMessage('response_log', str(work_data))

        if self.parsedRequest.needTrafficItem():
            self.saveTrafficItem(response)

        return response

    def obtainPrelandConfig(self):
        if self.landing['prelands_json'] and self.landing['prelands_json'] != '[]':
            self.landing['prelands_json'] = json.loads(self.landing['prelands_json'])
            self.prelandConfig['url'] = random.choice(self.landing['prelands_json'])
        else:
            return self.prelandConfig

        if 'show_preland' in self.landing and self.landing['show_preland']:
            self.prelandConfig['enable'] = True
            return self.prelandConfig

        try:
            stream_operator = DbHelper().getFrom('OperatorStreamPrelandSettings', str(self.parsedRequest.stream['id_stream']) + '_' + str(self.landing['id_operator'])).decode()
            if stream_operator:
                if stream_operator == 'hide':
                    self.prelandConfig['enable'] = False
                else:
                    self.prelandConfig['enable'] = True
                return self.prelandConfig
        except AttributeError:
            pass

        if self.parsedRequest.stream['prelands_json_referer'] and self.parsedRequest.stream['prelands_json_referer'] != '[]' and self.parsedRequest.ref:
            streamRef = json.dumps(self.parsedRequest.stream['prelands_json_referer'])

            for item in streamRef['show']:
                if item in self.parsedRequest.ref:
                    self.prelandConfig['enable'] = True
                    return self.prelandConfig

            for item in streamRef['hide']:
                if item in self.parsedRequest.ref:
                    self.prelandConfig['enable'] = False
                    return self.prelandConfig

        try:
            partner_operator = DbHelper().getFrom('OperatorUserPrelandSettings', str(self.parsedRequest.stream['id_partner']) + '_' + str(self.landing['id_operator'])).decode()
            if partner_operator:
                if partner_operator == 'hide':
                    self.prelandConfig['enable'] = False
                else:
                    self.prelandConfig['enable'] = True

                return self.prelandConfig
        except AttributeError:
            pass

        try:
            ref_partner = DbHelper().getFrom('UserReferrerSettings', str(self.parsedRequest.stream['id_partner']) + '_' + str(self.landing['id_operator'])).decode()
            if ref_partner and ref_partner != '[]' and self.parsedRequest.ref:
                parnterRef = json.dumps(ref_partner)

                for item in parnterRef['show']:
                    if item in self.parsedRequest.ref:
                        self.prelandConfig['enable'] = True
                        return self.prelandConfig

                for item in parnterRef['hide']:
                    if item in self.parsedRequest.ref:
                        self.prelandConfig['enable'] = False
                        return self.prelandConfig
        except AttributeError:
            pass

        self.prelandConfig['enable'] = True

        return self.prelandConfig

    def getRedirectType(self):
        if self.parsedRequest.fromScript:
            redirectType = 10
        elif self.parsedRequest.split['redirect_type'] != 0:
            redirectType = self.parsedRequest.split['redirect_type']
        else:
            redirectType = self.parsedRequest.stream['type_redirect']

        return redirectType

    def saveTrafficItem(self, response):
        item = Traffic()

        item.user_agent = self.parsedRequest.userAgent
        item.datetime = self.parsedRequest.datetime
        item.date = self.parsedRequest.date
        item.hours_id = self.parsedRequest.hoursId
        item.uniq_hash = self.parsedRequest.uniqHash
        item.ref = self.parsedRequest.ref
        item.ref_full = self.parsedRequest.refFull
        item.hours_id = self.parsedRequest.hoursId
        item.split_number = self.parsedRequest.splitOrder
        item.os = self.parsedRequest.osId
        item.os_ver = self.parsedRequest.osVersionId
        item.id_device_brand = self.parsedRequest.vendorId
        item.id_device_model = self.parsedRequest.deviceModelId
        item.device_type = self.parsedRequest.type
        item.browser = self.parsedRequest.browser
        item.ip = self.parsedRequest.ip
        item.id_operator = self.parsedRequest.operatorId
        item.ip_range_id = self.parsedRequest.ipRangeId
        item.id_country = self.parsedRequest.countryId

        item.sub1 = self.parsedRequest.sub1
        item.sub2 = self.parsedRequest.sub2
        item.sub3 = self.parsedRequest.sub3
        item.sub4 = self.parsedRequest.sub4
        item.sub5 = self.parsedRequest.sub5

        if self.parsedRequest.stream:
            item.id_source = self.parsedRequest.stream['id_stream']
            item.id_partner = self.parsedRequest.stream['id_partner']
            item.id_category = self.parsedRequest.stream['id_category']

        if self.landing:
            item.id_land = self.landing['id_land']
            item.id_agregator = self.landing['id_agregator']
            item.currency = self.landing['currency']
            item.is_valid = True
            if self.direct:
                if self.prelandConfig['enable']:
                    item.visit_land = 0
                    item.visit_preland = 1
                else:
                    item.visit_land = 1
                    item.visit_preland = 0
            else:
                item.visit_land = 0
                item.visit_preland = 0
        else:
            item.is_valid = False
            if self.parsedRequest.isValid():
                item.tb_reason = 4
            else:
                item.tb_reason = self.parsedRequest.tbReason

        item.cookie_value = int(self.parsedRequest.cookieValue)-1
        if self.parsedRequest.cookieSetDateTime:
            item.cookie_set_datetime = self.parsedRequest.cookieSetDateTime
        else:
            item.cookie_set_datetime = '2007-07-07 07:07:07'

        if hasattr(response, 'location'):
            item.location = response.location
        elif self.landing:
            item.location = self.landing['land_url']

        item.save(force_insert=True)

    @staticmethod
    def getGlobalSettings():
        return json.loads(DbHelper().get('GlobalSettings').decode())

    @classmethod
    def redirectToLand(cls, uniqHash):
        try:
            trafficItem = Traffic.select().where(Traffic.uniq_hash == uniqHash).limit(1).get()
        except Exception as e:
            LogHelper().infoMessage('redirect_log', 'traffic item not found: ' + uniqHash)
            trafficItem = False

        response = None

        if trafficItem:
            redisRecord = DbHelper().get('LinkFreshesPreland:' + str(uniqHash))
            stream = json.loads(DbHelper().getFrom('TDSStream', trafficItem.id_source).decode())
            if redisRecord:
                redisRecord = json.loads(redisRecord.decode())
                trafficItem.before_update_record()
                trafficItem.visit_land = 1
                trafficItem.location = redisRecord['land_url']
                trafficItem.save()
                response = web.HTTPMovedPermanently(redisRecord['land_url'])
            elif stream:
                trafficItem.before_update_record()
                trafficItem.location = stream['tb_url']
                trafficItem.is_valid = 0
                trafficItem.tb_reason = '5'
                trafficItem.visit_land = 0
                trafficItem.save()
                response = web.HTTPMovedPermanently(stream['tb_url'])

        if not response:
            globalSettings = cls.getGlobalSettings()
            response = web.HTTPMovedPermanently(globalSettings['global_tb_url'])

        work_data = {
            'location': response.location
        }
        LogHelper().infoMessage('redirect_log', str(work_data) + 'hash: ' + uniqHash)

        return response

    @classmethod
    def redirect(cls, uniqHash):
        try:
            trafficItem = Traffic.select().where(Traffic.uniq_hash == uniqHash).limit(1).get()
        except Exception as e:
            LogHelper().infoMessage('redirect_log', 'traffic item not found: ' + uniqHash)
            trafficItem = False

        response = None
        globalSettings = cls.getGlobalSettings()
        response = None

        if trafficItem:
            redisRecord = DbHelper().get('linkFreshesAD:' + str(uniqHash))
            stream = json.loads(DbHelper().getFrom('TDSStream', trafficItem.id_source).decode())
            if redisRecord:
                redisRecord = json.loads(redisRecord.decode())
                if redisRecord['redirect_to'] == 'preland':
                    trafficItem.before_update_record()
                    trafficItem.visit_preland = 1
                    trafficItem.location = redisRecord['preland_url']
                    trafficItem.save()
                    dataForRedis = {
                        'redirect_type': 'script',
                        'redirect_to': 'land',
                        'timestamp': int(time.time()),
                        'land_url': redisRecord['land_url'],
                    }
                    DbHelper().setAndExpire('LinkFreshesPreland:' + uniqHash,
                                            json.dumps(dataForRedis), 300)
                    response = web.HTTPMovedPermanently(redisRecord['preland_url'])
                else:
                    trafficItem.before_update_record()
                    trafficItem.visit_land = 1
                    trafficItem.location = redisRecord['land_url']
                    trafficItem.save()
                    response = web.HTTPMovedPermanently(redisRecord['land_url'])
            elif stream:
                trafficItem.before_update_record()
                trafficItem.location = stream['tb_url']
                trafficItem.tb_reason = '7'
                trafficItem.save()
                response = web.HTTPMovedPermanently(stream['tb_url'])
            else:
                trafficItem.before_update_record()
                trafficItem.location = globalSettings['global_tb_url']
                trafficItem.is_valid = 0
                trafficItem.tb_reason = '7'
                trafficItem.save()

        if not response:
            response = web.HTTPMovedPermanently(globalSettings['global_tb_url'])

        work_data = {
            'location': response.location
        }
        LogHelper().infoMessage('scripts_redirect_log', str(work_data) + 'hash: ' + uniqHash)

        return response
