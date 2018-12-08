from components.LandChooser import LandChooser
from components.RequestParser import RequestParser
from components.PreparatoryResponse import PreparatoryResponse
from aiohttp import web
from dbModels import db
import time
from helpers import DbHelper, SmartRotatorHelper


async def by_hash_and_parameter(Request):
    db.manual_close()
    direct = str(Request.match_info.get('parameter')) == '1'

    parsedRequest = RequestParser(Request, shash=Request.match_info.get('hash'))
    landing = await LandChooser(parsedRequest).getLanding()
    response = PreparatoryResponse(parsedRequest, landing, direct=direct).getResponse()

    return response


async def by_hash(Request):
    db.manual_close()
    direct = False

    parsedRequest = RequestParser(Request, shash=Request.match_info.get('hash'))
    landing = await LandChooser(parsedRequest).getLanding()
    response = PreparatoryResponse(parsedRequest, landing, direct=direct).getResponse()

    return response

async def route(Request):
    db.manual_close()
    shash = Request.GET['hash']
    direct = (Request.GET['type'] if 'type' in Request.GET else '') == 'direct'

    parsedRequest = RequestParser(Request, shash=shash)
    landing = await LandChooser(parsedRequest).getLanding()
    response = PreparatoryResponse(parsedRequest, landing, direct=direct).getResponse()

    return response

async def get_script(Request):
    db.manual_close()
    direct = False
    data = await Request.json()

    parsedRequest = RequestParser(Request, shash=Request.GET['hash'], fromScript=True, data=data)
    landing = await LandChooser(parsedRequest).getLanding()
    response = PreparatoryResponse(parsedRequest, landing, direct=direct).getResponse()

    return response


async def redirect_to_land(Request):
    db.manual_close()
    uniqHash = Request.GET['to']
    resonse = PreparatoryResponse.redirectToLand(uniqHash=uniqHash)

    return resonse


async def redirect(Request):
    db.manual_close()
    uniqHash = Request.GET['to']
    resonse = PreparatoryResponse.redirect(uniqHash=uniqHash)

    return resonse


async def return_200(Request):
    return web.Response(text="have a good day)")


async def check_working_capacity(Request):
    db.manual_close()
    try:
        time1 = int(time.time())
        if not DbHelper().checkMysql():
            return web.Response(text="mysql not working", status=500)
        time2 = int(time.time())
        if not DbHelper().checkRdis():
            return web.Response(text="redis not working", status=500)
        time3 = int(time.time())
        # if not await SmartRotatorHelper.checkRotator():
        #     return web.Response(text="smart rotator not working", status=500)
        time4 = int(time.time())
    except Exception:
        return web.Response(text="something not working", status=500)

    return web.Response(text="all right; db: " + str(time2-time1) + " cash: " + str(time3-time2) + " sr: " + str(time4-time3))

