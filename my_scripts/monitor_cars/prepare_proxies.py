import json

countries = [
    'Austria',
    'Azerbaijan',
    'Armenia',
    'Belarus',
    'Bulgaria',
    'Hungary',
    'Vietnam',
    'Germany',
    'Greece',
    'Georgia',
    'Denmark',
    'Dominican Republic',
    'Egypt',
    'Israel',
    'Spain',
    'Italy',
    'Kazakhstan',
    'Cyprus',
    'Kyrgyzstan',
    'Cuba',
    'Latvia',
    'Lithuania',
    'Moldova',
    'Netherlands',
    'Norway',
    'Poland',
    'Portugal',
    'Russia',
    'Romania',
    'Serbia',
    'Slovakia',
    'Slovenia',
    'Tajikistan',
    'Thailand',
    'Tunisia',
    'Turkmenistan',
    'Turkey',
    'Uzbekistan',
    'Ukraine',
    'Finland',
    'France',
    'Montenegro',
    'Czech Republic',
    'Switzerland',
    'Estonia',
]

s = set()

with open('not_formated proxies.txt', 'r') as f:
    try:
        while 1:
            tt = f.readline()
            if not tt:
                break

            assepted = False
            for assepted_c in countries:
                if assepted_c.lower() in tt.lower():
                    assepted = True
                    break
            if not assepted or not ('https' in tt.lower() or 1):
                continue
            li = tt.split('\t')
            ip = li[0]
            port = li[1]
            if ':' in ip:
                li = ip.split(':')
                ip = li[0]
                port = li[1]
            s.add(tuple([ip.strip(), port.strip()]))
    except Exception as e:
        pass

with open('app\\proxy_list.json', 'w') as e:
    json.dump(list(s), e)

print(len(s))