from datetime import datetime
from urllib import parse
from hashlib import md5
from .AgregatorRegister import AgregatorRegister
from .Base import Base


class MTBillHelper(Base, metaclass=AgregatorRegister):
    agregatorId = 2
    MTBillPassword = 'Dbjk4uWnmQaZn'

    @classmethod
    async def getLandingUrl(cls, landing, parsedRequest, session):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = {
            'url': landing['land_url']+'&time='+parse.quote_plus(date) +
                   '&nopreland=1&sign=' + md5(cls.MTBillPassword+date+'1').hexdigest()
        }

        return result

