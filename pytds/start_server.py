from server import run_server
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--port')
parser.add_argument('--host')

if __name__ == '__main__':
    port = parser.parse_args().port
    port = int(port) if port else 8080
    host = parser.parse_args().host
    host = str(host) if host else '127.0.0.1'
    run_server(host, port)
