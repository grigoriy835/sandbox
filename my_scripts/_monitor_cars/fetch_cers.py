import requests
from bs4 import BeautifulSoup
from lxml import html


sources = [
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/nissan/note/peredniy_privod-ASgBAQICAkTgtg36mCjitg3yqygBQO62DRTmtyg?f=ASgBAQECA0TyCrCKAeC2DfqYKOK2DfKrKAFA7rYNFOa3KAJF~AIXeyJmcm9tIjoyODQ0LCJ0byI6bnVsbH3GmgwWeyJmcm9tIjowLCJ0byI6NTUwMDAwfQ&radius=200&user=1'
    }
]


def parse_avito(url):
    def is_a_item(tag):
        return tag.has_attr('data-marker') and tag['data-marker'] == 'catalog-serp'

    page = requests.get(url)
    soup = BeautifulSoup(page.text)
    items = list(soup.find_all(is_a_item).pop().children)
    return items


def parse_autoru(url):
    pass


def parse_drom(url):
    pass


for source in sources:
    if source['type'] == 'avito':
        items = parse_avito(source['url'])
