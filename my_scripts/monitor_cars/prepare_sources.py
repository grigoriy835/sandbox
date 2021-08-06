import json


sources = [
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/nissan/tiida-ASgBAgICAkTgtg36mCjitg2Usig?f=ASgBAgICA0TyCrCKAeC2DfqYKOK2DZSyKA&localPriority=1&radius=100',
        'info': 'nissan tiida all in 100kmk'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/nissan/note/levyy_rul-ASgBAQICAkTgtg36mCjitg3yqygBQPAKFKyKAQ?f=ASgBAQICA0TyCrCKAeC2DfqYKOK2DfKrKAFA8AoUrIoB&radius=100&localPriority=1',
        'info': 'nissan note all in 100kmk'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/skoda/fabia/levyy_rul-ASgBAQICAkTgtg2emSjitg2IpSgBQPAKFKyKAQ?f=ASgBAQECAkTgtg2emSjitg2IpSgBQPAKFKyKAQFFxpoMFnsiZnJvbSI6MzUwMDAwLCJ0byI6MH0&localPriority=1&radius=100',
        'info': 'fabia from 350k in 100kmk'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/suzuki/swift/levyy_rul-ASgBAQICAkTgtg2omSjitg3MsSgBQPAKFKyKAQ?f=ASgBAQECA0TyCrCKAeC2DaiZKOK2DcyxKAFA8AoUrIoBAUXGmgwWeyJmcm9tIjozNTAwMDAsInRvIjowfQ&localPriority=1&radius=100',
        'info': 'suzuki swift from 350k in 100kmk'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/renault/sandero_1429/levyy_rul-ASgBAQICAkTgtg2MmSjitg3ErygBQPAKFKyKAQ?f=ASgBAQECA0TyCrCKAeC2DYyZKOK2DcSvKAFA8AoUrIoBAkX4Ahh7ImZyb20iOjEzOTc4LCJ0byI6bnVsbH3GmgwbeyJmcm9tIjozNTAwMDAsInRvIjo2MDAwMDB9&localPriority=1&radius=100',
        'info': 'Renault Sandero 2015+ from 350k-600k in 100km'
    },
    {
        'type': 'avito',
        'url': 'https://www.avito.ru/nizhniy_novgorod/avtomobili/opel/astra/levyy_rul-ASgBAQICAkTgtg3~mCjitg3cnigBQPAKFKyKAQ?f=ASgBAQECA0TyCrCKAeC2Df6YKOK2DdyeKAFA8AoUrIoBAUXGmgwbeyJmcm9tIjozNTAwMDAsInRvIjo2MDAwMDB9&localPriority=1&radius=100',
        'info': 'opel astra j from 350k-600k in 100km'
    },


    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/all/?price_to=600000&catalog_filter=mark%3DNISSAN%2Cmodel%3DTIIDA&catalog_filter=mark%3DNISSAN%2Cmodel%3DNOTE&sort=cr_date-desc&price_from=350000&geo_radius=100',
        'info': 'nissan note/tiida all in 100kmk'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/skoda/fabia/all/?price_from=350000&price_to=600000&sort=cr_date-desc&geo_radius=100',
        'info': 'fabia 350-600 in 100kmk'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/renault/sandero-sandero/all/?price_from=350000&price_to=600000&sort=cr_date-desc&year_from=2014&geo_radius=100',
        'info': 'Renault Sandero 2014+ 350-600 in 100kmk'
    },
    {
        'type': 'autoru',
        'url': 'https://auto.ru/nizhniy_novgorod/cars/opel/astra-astra/all/?price_from=350000&price_to=600000&sort=cr_date-desc&geo_radius=100',
        'info': 'opel astra j 2014+ 350-600 in 100kmk'
    },



]

with open('app\sources.json', 'w') as f:
    json.dump(sources, f, indent=4)
