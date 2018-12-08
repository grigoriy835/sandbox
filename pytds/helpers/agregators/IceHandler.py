from dbModels import IceSubIdTables
from .AgregatorRegister import AgregatorRegister
from .Base import Base


class IceHandler(Base, metaclass=AgregatorRegister):
    agregatorId = 9

    @staticmethod
    async def getLandingUrl(landing, parsedRequest, session):
        subId = IceSubIdTables()
        subId.uniq_hash = parsedRequest.uniqHash
        subId.save(force_insert=True)

        result = {
            'url': landing['land_url'].replace('{click_id}', str(subId.id))
        }

        return result
