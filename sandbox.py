s = set()

with open('my_scripts/monitor_cars/proxy_list.txt', 'r') as f:
    try:
        while 1:
            tt = f.readline()
            if 'United' in tt:
                continue
            if 'Canada' in tt:
                continue
            if 'Brazil' in tt:
                continue
            if 'Australia' in tt:
                continue
            if 'Indonesia' in tt:
                continue
            if 'India' in tt:
                continue
            if not tt:
                break
            if 'HTTPS' in tt or 'https' in tt:
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

with open('my_scripts/monitor_cars/normalized_proxy_list.txt', 'w') as e:
    e.write(str(s))

print(len(s))