from .AgregatorRegister import AgregatorRegister
from dbModels import NMSMTSubsRedirect
from datetime import datetime
from .Base import Base


class NMSMTHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 8

    @staticmethod
    async def getLandingUrl(landing, parsedRequest, session):
        result = {
            'url': landing['nms_land_url'].replace('{hash}', parsedRequest.uniqHash),
            'subId': landing['id_land'],
        }

        return result

    @staticmethod
    def saveSubId(hash, subId):
        NMSMTSubsRedirect.insert(uniq_hash=hash, landing_id=subId, datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), request_id='', phone='')
