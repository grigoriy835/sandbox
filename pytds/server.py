from handlers import *
from helpers import LogHelper

app = web.Application()
app['instance_prefix'] = ''

app.router.add_get('/favicon.ico', return_200)
app.router.add_get('/', return_200)

app.router.add_get('/redirect_to_land', redirect_to_land)
app.router.add_get('/redirect', redirect)

app.router.add_get('/getscript', get_script)
app.router.add_get('/{hash}.js', by_hash)
app.router.add_get('/{hash}/{parameter}', by_hash_and_parameter)
app.router.add_get('/route', route)

app.router.add_get('/check_tds', check_working_capacity)

LogHelper()


def run_server(host, port):
    app['instance_prefix'] = port
    web.run_app(app, host=host, port=port)
