# просто получаем с ротатора pure_bandit рейтинги по потоку (редактировать переменные чтобы сменить поток и пр.)
import requests
import json

smartRotatorUrl = 'http://apimobi.com:1234/'

id_stream = 1051
operator_id = 25
cookieValue = 1

streamHash = int(id_stream) * 1000000 + int(operator_id) * 100 \
             + int(cookieValue)

params = [streamHash]

headers = {'content-type': 'application/json'}
data = {
    'jsonrpc': "2.0",
    'id': 0,
    'method': 'mabserver.pure_bandit',
    'params': params
}

response = requests.post(smartRotatorUrl, data=json.dumps(data), headers=headers, timeout=5)

print(response.json())