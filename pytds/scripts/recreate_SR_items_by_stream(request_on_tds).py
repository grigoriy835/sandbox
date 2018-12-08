# отправляем запрос на тдс как это делает партнёрка при вкл/выкл ротатора или редактировании стрима
import requests
import json
from hashlib import md5
from urllib import parse

url = 'http://apimobi.com/smart_rotator_create_source'

id_stream = 1051
s_word = 'SMOKEweedEVRYDAY'
key = '12345'

url += '?id_stream=' + str(id_stream) + '&key=' + key + '&hash=' + parse.quote_plus(md5((key + s_word).encode()).hexdigest())

print(str(url))
response = requests.get(url)

print(response.text)
