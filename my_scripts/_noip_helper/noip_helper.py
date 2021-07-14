from aiohttp import web
from aiohttp.web_request import Request
import sys
from logging import getLogger

from aiohttp.web_response import Response

port = 8000
filename = 'cur_ip'


async def save_new_ip(request: Request) -> Response:
    peername = request.transport.get_extra_info('peername')
    if peername:
        ip = peername[0]

        with open(filename, 'w') as f:
            f.truncate()
            f.write(ip)
        getLogger(__name__).warning(f'new ip setted {ip}')

    return web.Response()


async def redirect_to(request: Request) -> Response:
    global port
    try:
        with open(filename, 'r') as f:
            ip = f.read()
        return web.HTTPFound(f'http://{ip}:{port}')
    except Exception:
        return web.Response()


app = web.Application()
app.router.add_get('/', redirect_to)
app.router.add_get('/save_new_ip', save_new_ip)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = sys.argv[1]
    web.run_app(app, port=port)
