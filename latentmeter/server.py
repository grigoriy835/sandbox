from aiohttp import web

app = web.Application()
app['instance_prefix'] = ''


def run_server(host, port):
    app['instance_prefix'] = port
    web.run_app(app, host=host, port=port)
