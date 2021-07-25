import json
import os
import requests
from bs4 import BeautifulSoup, Tag
from typing import List, Dict
import hashlib
import time
import random


chat_id = -510251579
avito_notified = False

with open('proxy_list.json', 'wr') as f:
    proxy_list = json.load(f)

sources = [
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili?f=ASgBAQECA0TyCrCKAeC2DYyZKOK2DfCjKAJA7rYNFOa3KPC2DRTstygCRfgCF3siZnJvbSI6Mjg0NCwidG8iOm51bGx9xpoMFnsiZnJvbSI6MCwidG8iOjU1MDAwMH0&radius=100&user=1',
        'info': 'рено дастер'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili?f=ASgBAQECA0TyCrCKAeC2DaiZKOK2DcyxKAJA7rYNFOa3KPC2DRTstygCRfgCF3siZnJvbSI6Mjg0NCwidG8iOm51bGx9xpoMFnsiZnJvbSI6MCwidG8iOjU1MDAwMH0&radius=100&user=1',
        'info': 'сузуки свифт до 550'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili?f=ASgBAQECA0TyCrCKAeC2DZ6ZKOK2DYilKAJA7rYNFOa3KPC2DRTstygCRfgCF3siZnJvbSI6Mjg0NCwidG8iOm51bGx9xpoMFnsiZnJvbSI6MCwidG8iOjU1MDAwMH0&radius=100&user=1',
        'info': 'шкода фабий'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili?f=ASgBAQECA0TyCrCKAeC2DcqYKOK2DaqhKAJA7rYNFOa3KPC2DRTstygCRfgCF3siZnJvbSI6Mjg0NCwidG8iOm51bGx9xpoMFnsiZnJvbSI6MCwidG8iOjU1MDAwMH0&radius=100&user=1',
        'info': 'киа серато'
    },
    {

        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili?f=ASgBAQECA0TyCrCKAeC2DcqYKOK2DZShKAJA7rYNFOa3KPC2DRTstygCRfgCF3siZnJvbSI6Mjg0NCwidG8iOm51bGx9xpoMFnsiZnJvbSI6MCwidG8iOjU1MDAwMH0&radius=100&user=1',
        'info': 'киа сид'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/skoda/octavia/peredniy_privod-ASgBAQICAkTgtg2emSjitg2ErCgBQO62DRTmtyg?f=ASgBAQECA0TyCrCKAeC2DZ6ZKOK2DYSsKAFA7rYNFOa3KAJF~AIXeyJmcm9tIjoyODQ0LCJ0byI6bnVsbH3GmgwWeyJmcm9tIjowLCJ0byI6NTUwMDAwfQ&radius=100&user=1',
        'info': 'октавиа механника и робот'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili?f=ASgBAQECA0TyCrCKAeC2DfqYKOK2DfKrKAJA7rYNFOa3KPC2DRTstygCRfgCF3siZnJvbSI6Mjg0NCwidG8iOm51bGx9xpoMFnsiZnJvbSI6MCwidG8iOjU1MDAwMH0&radius=100&user=1',
        'info': 'ниссан нот'
    },
    # autoru -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/suzuki/swift/used/?year_from=2010&price_from=350000&price_to=550000&transmission=MECHANICAL&geo_radius=100&sort=cr_date-desc',
        'info': 'сузуки свифт'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/kia/cerato/used/?year_from=2010&price_to=550000&sort=cr_date-desc&geo_radius=100&transmission=MECHANICAL',
        'info': 'киа серато'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/skoda/octavia/used/?year_from=2010&price_to=550000&transmission=MECHANICAL&transmission=ROBOT&geo_radius=100&sort=cr_date-desc',
        'info': 'октавиа механника и робот'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/skoda/fabia/used/?year_from=2010&displacement_from=1400&transmission=MECHANICAL&geo_radius=100&sort=cr_date-desc&price_to=550000',
        'info': 'шкода фабий'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/kia/ceed/used/?geo_radius=100&year_from=2010&price_from=400000&price_to=550000&displacement_from=1400&transmission=MECHANICAL',
        'info': 'киа сид'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/renault/duster/used/?year_from=2010&price_from=300000&price_to=550000&transmission=MECHANICAL&geo_radius=100&sort=cr_date-desc',
        'info': 'сузуки свифт'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/nissan/note/used/?year_from=2010&price_from=300000&price_to=550000&sort=cr_date-desc&geo_radius=100&transmission=MECHANICAL',
        'info': 'ниссан ноут'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/vendor-foreign/all/?year_from=2018&price_from=500000&price_to=600000&geo_radius=100&sort=cr_date-desc&transmission=MECHANICAL',
        'info': 'foreign cars > 2018 year'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/ford/focus/used/?year_from=2012&price_from=400000&price_to=550000&geo_radius=100&transmission=MECHANICAL&sort=cr_date-desc',
        'info': 'autoru ford_focus > 2012'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili?f=ASgBAQECA0TyCrCKAeC2DZyYKOK2DcKlKAJA7rYNFOa3KPC2DRTstygDRfgCF3siZnJvbSI6Mjg0NCwidG8iOm51bGx9vBUYeyJmcm9tIjoxNTc4NiwidG8iOm51bGx9xpoMG3siZnJvbSI6NDAwMDAwLCJ0byI6NTUwMDAwfQ&radius=100&user=1',
        'info': 'avito ford_focus > 2012'
    },

    
]



class hashabledict(dict):
    def __hash__(self):
        return int(self['id'])

    @classmethod
    def from_dict(cls, item: dict):
        new_item = cls()
        for k, v in item.items():
            new_item[k] = v

        return new_item


def parse_autoru(url) -> List[Dict]:
    def is_a_item(tag: Tag):
        return tag.name == 'div' and tag.has_attr('class') and 'ListingItem-module__container' in tag['class']

    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    items = list(soup.find_all(is_a_item))

    def map_func(item: Tag) -> dict:
        res = hashabledict()
        link = item.contents.pop().contents[1].find('a')['href']
        res['link'] = link
        res['id'] = int(hashlib.sha1(link.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

        return res

    return list(map(map_func, items))


def parse_avito(url) -> List[Dict]:
    user_as = [
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.7.01001)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.5.01003)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8',
        'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (X11; U; Linux x86_64; de; rv:1.9.2.8) Gecko/20100723 Ubuntu/10.04 (lucid) Firefox/3.6.8',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; .NET CLR 1.0.3705)',
        'Mozilla/5.0 (Windows NT 5.1; rv:13.0) Gecko/20100101 Firefox/13.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1',
        'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
        'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.01',
        'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (Windows NT 5.1; rv:5.0.1) Gecko/20100101 Firefox/5.0.1',
        'Mozilla/5.0 (Windows NT 6.1; rv:5.0) Gecko/20100101 Firefox/5.02',
        'Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1',
        'Mozilla/4.0 (compatible; MSIE 6.0; MSIE 5.5; Windows NT 5.0) Opera 7.02 Bork-edition [en]',
    ]
    def is_a_item(tag):
        return tag.parent.has_attr('data-marker') and tag.parent['data-marker'] == 'catalog-serp' and \
               tag.has_attr('data-marker') and tag['data-marker'] == 'item'

    def is_a_time_marker(tag):
        return tag.has_attr('data-marker') and tag['data-marker'] == 'item-date'

    random.shuffle(proxy_list)
    page = False
    for proxy in proxy_list:
        random.shuffle(user_as)
        proxy_dict = {
            "https": f'http://{proxy[0]}:{proxy[1]}',
        }
        headers = {'User-Agent': user_as[0]}
        try:
            page = requests.get(url, proxies=proxy_dict, timeout=10, headers=headers)
        except Exception as e:
            continue
        if page.status_code != 200:
            continue
        else:
            break
    if not page or page.status_code != 200:
        global avito_notified
        if not avito_notified:
            avito_notified = True
            requests.post('https://api.telegram.org/bot1868613248:AAGnE3Z3zj1H75z6KI6Nfr3kuzW-3LwIAUQ/sendMessage', json={
                'chat_id': chat_id,
                'text': f'cannot load avito page'
            })
        raise Exception(f'cant load page from avito {str(page)[:50]}')

    soup = BeautifulSoup(page.text, 'html.parser')
    items = list(soup.find_all(is_a_item))

    def map_func(item: Tag) -> dict:
        res = hashabledict(id=int(item['data-item-id'].strip()))
        link = item.find('a')['href']
        res['link'] = f'https://www.avito.ru{link}'
        res['time'] = item.find(is_a_time_marker).contents.pop()

        return res

    return list(map(map_func, items))


def parse_drom(url) -> List[Dict]:
    # todo implement drom parsing
    return []


fun_mapping = {
    'drom': parse_drom,
    'avito': parse_avito,
    'autoru': parse_autoru,
}


def extract_new_records(old: List[Dict], actual: List[Dict]) -> List[Dict]:
    new = set(actual) - set(old)
    return list(new)


def process_new_items(source: dict, new_items: List[Dict]) -> None:
    print(f'notifying about {len(new_items)} new items')
    for item in new_items:
        time = item["time"] if "time" in item and item['time'] else ""
        requests.post('https://api.telegram.org/bot1868613248:AAGnE3Z3zj1H75z6KI6Nfr3kuzW-3LwIAUQ/sendMessage', json={
            'chat_id': chat_id,
            'text': f'{time}{item["link"]}'
        })
    pass


def extract_old_records() -> Dict:
    path = 'old_records.json'
    try:
        if os.path.isfile(path):
            with open(path, 'r') as old_r_file:
                old = json.load(old_r_file)
                print('loaded odl list with items from file')
                for k, v in old.items():
                    old[k] = list(map(lambda x: hashabledict.from_dict(x), v))
                return old
        else:
            print(f'file {path} not exists, work without old info')
            return {}
    except Exception as e:
        print(f'cant load old json from {path} file')
    return {}


def save_new_actual_records(records: Dict) -> None:
    path = 'old_records.json'
    try:
        with open(path, 'w') as f:
            f.truncate()
            json.dump(records, f)
        print(f'new avtual items list saved to {path}')
    except Exception as e:
        print(f'cant dump old records to file {path}, not saved')


if __name__ == '__main__':
    old_records = extract_old_records()
    new_records_to_save = {}
    for id_ in range(0, len(sources)):
        source = sources[id_]
        id_ = str(id_)
        if source['type'] in fun_mapping:
            old_items = old_records[id_] if id_ in old_records else []
            try:
                actual_items = fun_mapping[source['type']](source['url'])
            except Exception as e:
                print(f'cant load actual records from {source["info"]}')
                continue
            new_items = extract_new_records(old_items, actual_items)
            print(f'{source["type"]} {source["info"]} old: {len(old_items)}, actual: {len(actual_items)}, new: {len(new_items)}')
            if len(new_items) == len(actual_items) and (len(actual_items) > 5 or id_ not in old_records):
                print(f'not notifying about {len(new_items)} items because it all actual or a new start for this url')
            else:
                process_new_items(source, new_items)

            new_records_to_save[id_] = actual_items
            time.sleep(5)

    save_new_actual_records(new_records_to_save)
