from os.path import join, dirname
from dotenv import load_dotenv
import os


dotenv_path = join(dirname(__file__), '.env')
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path)

appConfig = {
    'host': os.environ.get("CURRENT_HOST", 'pytds.local'),  # хост по которому доступен сервис
    'aggregator_receiver_host': os.environ.get("AGGREGATOR_HOST", 'localhost'),
}

mysqlConfig = {
    'main': {
        'connection': {
                'database': os.environ.get("DB_NAME", 'main'),
                'host': os.environ.get("DB_HOST", 'localhost'),
                'user': os.environ.get("DB_USER", 'root'),
                'passwd': os.environ.get("DB_PASSWORD", 'root'),
        },
    },
    'test': {
        'connection': {
            'database': 'main',
            'user': 'developer',
            'passwd': 'x25C1QOOi9nf',
            'host': '5.200.55.122',
        },
    }
}

redisConfig = {
    'main': {
        'connect': {
            'host': os.environ.get("REDIS_HOST", 'localhost'),
            'db': os.environ.get("REDIS_DB", 0),
            'password': os.environ.get("REDIS_PASSWORD", ''),
        }
    },
    'test': {
        'connect': {
            'host': 'localhost',
            'db': 2
        }
    }
}

rotatorConfig = {
    'main': {
        'smartRotatorUrl': os.environ.get("ROTATOR_URL", 'http://localhost:1234/'),
    },
    'test': {
        'smartRotatorUrl': 'http://localhost:1234/',
    }
}

agregatorsUrl = {
    'SDPays': 'http://api.sdpays.com/_subscription_create_wap.php',
    'PlanetThree': 'http://subscription-partners.i-free.ru/Http/Services/CreateSubscription.aspx',
    'MobileBaron': 'http://subs.mobilebaron.com/Http/Services/CreateSubscription.aspx',
    'PlanetThreeIC': 'https://callisto-merchant-api.pl3.com/API/XML/InvoiceManagementService.ashx',
    'FBilling': 'http://go.fbilling.com/subscription/init',
    'NMS': {
        32: 'http://azwapclick.com/azercell_msisdn',
        'other': 'http://azwapclick.com/landing',
    },
    'Pegas': 'http://pegasmoney.com/api3/',
    'InformPay': {
        24: 'http://bb.informpay.com/api?',
        25: 'http://pp.informpay.com/api?',
        27: 'http://tt.informpay.com/api?',
        28: 'http://mm.informpay.com/api?'
    },
    'PaymentTools': 'http://api.sub.payments.tools/wapclick',
    'ClickBerry': 'http://api.clickberry.xyz/subs/',
}
