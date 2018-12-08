from datetime import datetime
import json
from dbModels import AgregatorRequestError


class Base:
    agregatorId = None

    @classmethod
    def storeError(cls, request, response, errorMessage):
        date = datetime.now()
        errorData = {
            'agregator_id': cls.agregatorId,
            'request': json.dumps(request),
            'response': response,
            'error_text': errorMessage,
            'datetime': date.strftime("%Y-%m-%d %H:%M:%S"),
            'date': date.strftime("%Y-%m-%d"),
            'hours_id': int(date.strftime("%H")) + 1,
        }
        AgregatorRequestError.insert(**errorData).execute()
