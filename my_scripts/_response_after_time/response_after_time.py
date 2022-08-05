from aiohttp import web
from aiohttp.web_request import Request
import asyncio
import logging

from aiohttp.web_response import Response

app = web.Application()


async def sleep_n_response(request: Request) -> Response:
    sleep = request.query.get('sleep', False)
    response = request.query.get('response', '')

    print(response)
    if sleep:
        await asyncio.sleep(int(sleep))

    return web.Response(text=response)

app.router.add_get('/', sleep_n_response)
logging.basicConfig(level=logging.DEBUG)


def run_server(host, port):
    web.run_app(app, host=host, port=port)


if __name__ == '__main__':
    run_server(None, 9890)
