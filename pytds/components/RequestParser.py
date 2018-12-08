import GeoIP
import hashlib
import datetime
import ipaddress
import json
import uuid
from dbModels import OperatorsIP, CountryList, OSList, OSVersionList, VendorList, DeviceModelList, BrowserList
from urllib.parse import urlparse
from helpers import DbHelper, LogHelper
from peewee import DoesNotExist
from user_agents import parse
import socket


class RequestParser:
    hasPaymentToolsError = False

    request = None
    fromScript = False
    hash = None
    chosenLand = None

    useprlp = None

    hoursId = None
    datetime = None
    date = None
    userData = None
    userAgent = ''
    ip = ''
    operator = None
    operatorId = None
    ipRangeId = None
    countryCode = None
    countryName = None
    countryId = None
    osId = None
    osVersionId = None
    vendorId = None
    deviceModelId = None
    type = None
    browser = None
    ref = ''
    refFull = ''
    cookieName = None
    cookieValue = None
    cookieSetDateTime = None
    cookiesLiveTime = 0
    stream = None    # словарь со стримом либо None(если None то реквет не валидный)
    split = None  # словарь со сплитом либо None(если None то реквет не валидный)
    splitOrder = None
    uniqHash = None
    sub1 = None
    sub2 = None
    sub3 = None
    sub4 = None
    sub5 = None

    valid = None
    tbReason = None

    unknownDeviceTypes = {
        0: 'Unknown device',
        1: 'Unknown mobile',
        2: 'Unknown desktop',
        3: 'Unknown tablet'
    }

    def __init__(self, request, fromScript=False, shash='', data=None):
        self.uniqHash = str(request.app['instance_prefix']) + uuid.uuid4().hex
        LogHelper().infoMessage('parser', 'start hash ' + self.uniqHash)
        LogHelper().infoMessage('clients_info_log', '\nhash ' + self.uniqHash + '\nuser headers: ' + str(request.headers) + '\n user cookies: ' + str(request.cookies))

        self.request = request
        self.fromScript = fromScript
        self.hash = shash

        if 'landing' in request.GET:
            self.chosenLand = request.GET['landing']

        # кастомный аттрибут для cliclberry
        if 'useprlp' in request.GET:
            self.useprlp = request.GET['useprlp']

        source = DbHelper().getFrom('TDSSourceList', shash)
        if source:
            self.stream = json.loads(DbHelper().getFrom('TDSStream', source).decode('utf8'))
        if not self.stream:
            self.valid = False
            LogHelper().infoMessage('parser', 'no stream, hash: ' + self.uniqHash + ' shash: ' + shash)
            return

        now = datetime.datetime.now()
        self.hoursId = now.hour+1
        self.datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date = now.strftime("%Y-%m-%d")

        self.initCookies()

        if fromScript:
            self.userData = data

            if 'HTTP_USER_AGENT' in data:
                self.userAgent = data['HTTP_USER_AGENT']
            else:
                self.valid = False
                return

            if 'HTTP_X_FORWARDED_FOR' in data and data['HTTP_X_FORWARDED_FOR'] and '.' in data['HTTP_X_FORWARDED_FOR']:
                if ',' in data['HTTP_X_FORWARDED_FOR']:
                    self.ip = data['HTTP_X_FORWARDED_FOR'].split(',')[0].strip()
                else:
                    self.ip = data['HTTP_X_FORWARDED_FOR'].strip()
            if not self.ip:
                self.ip = data['REMOTE_ADDR']

            if 'Referer' in data:
                self.ref = urlparse(data['Referer']).netloc
                self.refFull = data['Referer']
            else:
                self.ref = self.refFull = ''

        else:
            if 'User-Agent' in request.headers:
                self.userAgent = request.headers['User-Agent']
            else:
                self.valid = False
                LogHelper().infoMessage('parser', 'no user agent, hash: ' + self.uniqHash + ' shash: ' + shash)
                return

            if 'X-Forwarded-For' in request.headers:
                self.ip = request.headers['X-Forwarded-For'].split(',')[0]
            else:
                peername = request.transport.get_extra_info('peername')
                if peername is None:
                    self.valid = False
                    LogHelper().infoMessage('parser', 'no peername, hash: ' + self.uniqHash + ' shash: ' + shash)
                    return

                self.ip, port = peername

            if 'Referer' in request.headers:
                self.ref = urlparse(request.headers['Referer']).netloc
                self.refFull = request.headers['Referer']
            else:
                self.ref = self.refFull = ''

        # if 'ip' in request.GET:  # debug
        #     self.ip = request.GET['ip']
        #     self.userAgent = 'Mozilla/5.0 (Linux; Android 4.4.2; SM-G350E Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.109 Mobile Safari/537.36'

        gi = GeoIP.new(GeoIP.GEOIP_MEMORY_CACHE)
        self.countryCode = gi.country_code_by_addr(self.ip)
        if not self.countryCode:
            self.countryCode = 'Unknown'
        self.countryName = gi.country_name_by_addr(self.ip)
        if not self.countryName:
            self.countryName = 'Unknown'
        self.countryId = DbHelper().getFrom('CountryList', self.countryCode)
        if not self.countryId:
            country = CountryList()
            country.name = self.countryName
            country.isoCode = self.countryCode
            country.save(force_insert=True)
            self.countryId = country.country_id
            DbHelper().setTo('CountryList', self.countryCode, country.country_id)

        try:
            intIP = int(ipaddress.ip_address(self.ip))
        except ValueError:
            intIP = 0


        try:
            self.operator = OperatorsIP.select().where(OperatorsIP.start <= intIP).where(OperatorsIP.end >= intIP).where(OperatorsIP.deleted_at == None).get()
            self.operatorId = self.operator.operator_id
            self.ipRangeId = self.operator.id
        except DoesNotExist:
            self.operator = False
            self.ipRangeId = 0
            ip = self.ip
            if 'X-Forwarded-For' in request.headers:
                ip = request.headers['X-Forwarded-For']
            LogHelper().infoMessage('parser', 'operator detection failed, hash: ' + self.uniqHash + ' shash: ' + shash + ' ip: ' + str(ip))

            try:
                socket.inet_aton(self.ip)
            except socket.error:
                self.ip = '0.0.0.0'
            return

        split = DbHelper().getFrom('TDSSplit', str(self.stream['id_stream'])+'_'+str(self.cookieValue))
        if split:
            split = json.loads(split.decode('utf8'))
            if split['os_array'] != 'all':
                split['os_array'] = json.loads(split['os_array'])
            if split['browser_array'] != 'all':
                split['browser_array'] = json.loads(split['browser_array'])
            split['land_array'] = json.loads(split['land_array'])
            split['device_type'] = json.loads(split['device_type'])
            self.splitOrder = split['split_order']
            self.split = split
        else:
            return

        self.parseAgent()

        try:
            self.deviceModelId = int(self.deviceModelId)
        except TypeError:
            self.deviceModelId = 0
        except ValueError:
            self.deviceModelId = 0
        try:
            self.vendorId = int(self.vendorId)
        except TypeError:
            self.vendorId = 0
        except ValueError:
            self.vendorId = 0

        self.sub1 = request.GET['sub1'] if 'sub1' in request.GET else ''
        self.sub2 = request.GET['sub2'] if 'sub2' in request.GET else ''
        self.sub3 = request.GET['sub3'] if 'sub3' in request.GET else ''
        self.sub4 = request.GET['sub4'] if 'sub4' in request.GET else ''
        self.sub5 = request.GET['sub5'] if 'sub5' in request.GET else ''
        LogHelper().infoMessage('parser', 'end hash ' + self.uniqHash)

    def isValid(self):
        if self.valid is None:
            if self.stream['status'] != 'active':
                self.tbReason = 1
                self.valid = False
                return self.valid

            if not self.operator:
                self.tbReason = 2
                self.valid = False
                return self.valid

            if not self.split:
                self.tbReason = 8
                self.valid = False
                return self.valid

            if self.operatorId == 29 or self.operatorId == 30 or self.operatorId == 32:
                if '[FB' in self.userAgent:  # мегафон дает пизды и штраф если в инн апп браузере подписать чувака
                    self.tbReason = 12
                    self.valid = False
                    return self.valid

            if str(self.type) not in self.split['device_type']:
                self.tbReason = 10
                self.valid = False
                return self.valid

            if self.split['os_array'] != 'all':
                if self.split['os_equal_type'] == 'equal' and self.osId not in self.split['os_array']:
                    self.tbReason = 9
                    self.valid = False
                    return self.valid
                if self.split['os_equal_type'] != 'equal' and self.osId in self.split['os_array']:
                    self.tbReason = 9
                    self.valid = False

                    return self.valid

            if self.split['browser_array'] != 'all':
                if self.split['browser_equal_type'] == 'equal' and self.browser not in self.split['browser_array']:
                    self.tbReason = 11
                    self.valid = False
                    return self.valid
                if self.split['browser_equal_type'] != 'equal' and self.browser in self.split['browser_array']:
                    self.tbReason = 11
                    self.valid = False
                    return self.valid

            if self.isBadReferrer():
                self.valid = False
                self.tbReason = 13
                return self.valid

            if (self.operatorId == 24 or self.operatorId == 25) and ('Micromax' in self.userAgent or 'Umi' in self.userAgent or 'BQ' in self.userAgent):
                self.valid = False
                self.tbReason = 15
                return self.valid

            lower_agent = self.userAgent.lower()

            if 'ht16' in lower_agent or 'ht30' in lower_agent or 'ht37' in lower_agent or 'fs454' in lower_agent or 'fs505' in lower_agent\
                    or 'fs517' in lower_agent or 'ht16' in lower_agent or 'ht7' in lower_agent or 'ht27' in lower_agent or 'ss830' in lower_agent\
                    or 'tele2 midi' in lower_agent or 'a42p' in lower_agent or 'ss350' in lower_agent or 't52p' in lower_agent\
                    or 'mtc smart start 2g' in lower_agent or 'nimbus 11' in lower_agent or 'fs456' in lower_agent or 'ff179' in lower_agent\
                    or 'nimbus 15' in lower_agent or 'cirrus 4' in lower_agent or 's453' in lower_agent:
                self.valid = False
                self.tbReason = 15
                return self.valid

            if self.fromScript and 'engines' in self.request.GET and self.request.GET != 'ygmhb':
                # todo проверить на соответствие поисковику 265 in original
                pass

            self.valid = True
        return self.valid

    def needTrafficItem(self):
        return True if self.isValid() or self.tbReason else False

    def initCookies(self):
        if self.chosenLand:
            self.cookieName = self.hash
            self.cookieValue = 1
        else:
            name = self.hash + '_' + hashlib.md5(self.ref.encode('utf-8')).hexdigest()
            self.cookieName = name
            self.cookieValue = int(self.request.cookies[name])+1 if name in self.request.cookies else 1
            if name+'_datetime' in self.request.cookies:
                self.cookieSetDateTime = self.request.cookies[name+'_datetime']
        self.cookiesLiveTime = self.stream['time_cookie'] * 60 if self.stream['time_cookie'] and self.stream['time_cookie'] <= 60 * 24 else 60 * 60 * 24

    def isBadReferrer(self):  # todo добавить чек на жесть 339
        if self.ref:
            badRefs = json.loads(DbHelper().get('BadRefererList').decode())
            for ref in badRefs:
                if ref in self.ref:
                    return True

            stopWords = json.loads(DbHelper().get('StopWords').decode())
            for word in stopWords:
                if word in self.refFull:
                    return True

    def parseAgent(self):
        cacheName = 'UACache:' + hashlib.md5(self.userAgent.encode('utf-8')).hexdigest()
        cache = DbHelper().get(cacheName)

        if cache:
            data = json.loads(cache.decode())
            self.type = data['type_device']
            self.osId = data['os']
            self.browser = data['browser']
            self.deviceModelId = data['model']
            self.osVersionId = data['os_ver']
            self.vendorId = data['type_device']
            return

        parsedAgent = parse(self.userAgent)

        osFamily = parsedAgent.os.family if parsedAgent.os.family else 'Unknown OS'
        versionString = parsedAgent.os.version_string if parsedAgent.os.version_string else 'Unknown'
        browserFamily = parsedAgent.browser.family if parsedAgent.browser.family else 'Unknown'

        if parsedAgent.is_mobile:
            self.type = 1
        if parsedAgent.is_pc:
            self.type = 2
        if parsedAgent.is_tablet:
            self.type = 3

        brand = parsedAgent.device.brand

        if not brand:  # костыль для китайфонов
            lowerAgent = self.userAgent.lower()
            if osFamily in ['Android', 'MocorDroid']:
                if 'mobile' in lowerAgent:
                    self.type = 1
                else:
                    self.type = 2
                self.osId = 1
            elif browserFamily in ['Android Browser']:
                if 'mobile' in lowerAgent:
                    self.type = 1
                else:
                    self.type = 2
            elif browserFamily in ['Opera Mini']:
                if 'mobile' in lowerAgent:
                    self.type = 1
                else:
                    self.type = 2

            if self.type == 2:
                for word in ['opera mini', 'opera mobi', 'symbos', 'j2me', 'android', 'iphone', 'symbian', 'windows phone', 'windows ce']:
                    if word in lowerAgent:
                        self.type = 2
                        break
        if not brand:
            if self.type in self.unknownDeviceTypes:
                brand = self.unknownDeviceTypes[self.type]
            else:
                brand = self.unknownDeviceTypes[0]

        model = parsedAgent.device.model
        if not model:
            if self.type in self.unknownDeviceTypes:
                model = self.unknownDeviceTypes[self.type]
            else:
                model = self.unknownDeviceTypes[0]

        self.osId = DbHelper().getFrom('NormalOSList', osFamily)
        if not self.osId:
            os = OSList()
            os.name = osFamily
            os.save(force_insert=True)
            self.osId = os.os_id
            DbHelper().setTo('NormalOSList', osFamily, self.osId)

        self.browser = DbHelper().getFrom('NormalBrowserList', browserFamily)
        if isinstance(self.browser, type(b'')):
            self.browser = self.browser.decode()
        if not self.browser:
            browser = BrowserList()
            browser.name = browserFamily
            browser.save(force_insert=True)
            self.browser = browser.browser_id
            DbHelper().setTo('NormalBrowserList', browserFamily, self.browser)

        self.osVersionId = self.getOsVersionId(versionString)

        self.vendorId = DbHelper().getFrom('VendorList', brand)
        if not self.vendorId:
            vendor = VendorList()
            vendor.name = brand
            vendor.save(force_insert=True)
            self.vendorId = vendor.vendor_id
            DbHelper().setTo('VendorList', brand, self.vendorId)

        self.deviceModelId = int(self.getDeviceModelId(model))

        data = {
            'user_agent': self.userAgent,
            'os': self.osId.decode() if isinstance(self.osId ,type(b'')) else self.osId,
            'os_ver': self.osVersionId.decode() if isinstance(self.osVersionId ,type(b'')) else self.osVersionId,
            'brand': self.vendorId.decode() if isinstance(self.vendorId ,type(b'')) else self.vendorId,
            'model': self.deviceModelId.decode() if isinstance(self.deviceModelId ,type(b'')) else self.deviceModelId,
            'type_device': self.type,
            'browser': self.browser.decode() if isinstance(self.browser ,type(b'')) else self.browser,
        }
        DbHelper().set(cacheName, json.dumps(data))

    def getDeviceModelId(self, name):
        if self.vendorId is None or not name:
            return None

        models = DbHelper().getFrom('DeviceModelList', self.vendorId)
        if models:
            models = json.loads(models.decode('utf-8'))
            for model in models:
                if model['name'] == name:
                    return model['device_model_id']
        else:
            models = []

        deviceModel = DeviceModelList()
        deviceModel.name = name
        deviceModel.vendor_id = self.vendorId.decode() if isinstance(self.vendorId, type(b'')) else self.vendorId
        deviceModel.save(force_insert=True)

        models.append(deviceModel.toDict())
        DbHelper().setTo('DeviceModelList', self.vendorId, json.dumps(models))

        return deviceModel.device_model_id

    def getOsVersionId(self, name):
        if self.osId is None or not name:
            return None

        versions = DbHelper().getFrom('OSVersionList', self.osId)
        if versions:
            versions = json.loads(versions.decode('utf-8'))
            for version in versions:
                if version['name'] == name:
                    return version['os_version_id']
                if isinstance(version['os_id'], type(b'')):
                    version['os_id'] = version['os_id'].decode()
        else:
            versions = []

        osVersion = OSVersionList()
        osVersion.name = name
        osVersion.os_id = self.osId.decode() if isinstance(self.osId, type(b'')) else self.osId
        osVersion.save(force_insert=True)

        versions.append(osVersion.toDict())
        DbHelper().setTo('OSVersionList', self.osId, json.dumps(versions))

        return osVersion.os_version_id
