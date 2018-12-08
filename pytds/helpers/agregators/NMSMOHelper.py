from .AgregatorRegister import AgregatorRegister
from dbModels import NMSMTSubsRedirect
from datetime import datetime
from .Base import Base


class NMSMOHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 8

    @staticmethod
    async def getLandingUrl(landing, parsedRequest, session):
        subItem = NMSMTSubsRedirect()
        subItem.uniq_hash = parsedRequest.uniqHash
        subItem.landing_id = landing['id_land']
        subItem.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        subItem.request_id = ''
        subItem.phone = ''
        subItem.save(force_insert=True)

        result = {
            'url': landing['nms_land_url'].replace('{code}', str(subItem.id))
        }

        return result
