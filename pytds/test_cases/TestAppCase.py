import os
os.environ['RUN_MOD'] = 'TEST'

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from handlers import *
from aiohttp import web


class TestAppCase(AioHTTPTestCase):
    def get_app(self, loop):
        app = web.Application(loop=loop)

        app.router.add_get('/favicon.ico', return_200)
        app.router.add_get('/', return_200)

        app.router.add_get('/getscript', get_script)
        app.router.add_get('/{hash}.js', by_hash)
        app.router.add_get('/{hash}/{parameter}', by_hash_and_parameter)

        return app

    @unittest_run_loop
    async def test_app(self):
        pass
        request = await self.client.request("GET", "/")
        assert request.status == 200
        request = await self.client.request("GET", "/4a8b3a32e343e589e2dc511636b6243b/1")  # id_stream = 1130
        assert request.status == 308
